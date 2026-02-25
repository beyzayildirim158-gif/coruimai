import express from 'express';
import cors from 'cors';
import path from 'node:path';
import fs from 'node:fs/promises';
import { z } from 'zod';
import puppeteer from 'puppeteer';
import { config } from './config.js';
import { logger } from './logger.js';
import { generatePDF, cleanupGenerator } from './pdf.js';
import { savePdf } from './storage.js';

// 🆕 Screenshot-based PDF generation - Frontend'i birebir yakalar
async function generateScreenshotPDF(
  analysisId: string, 
  sections?: string[],
  locale: string = 'tr'
): Promise<Buffer> {
  const frontendUrl = process.env.FRONTEND_URL || 'http://frontend:3000';
  const sectionsParam = sections ? `&sections=${sections.join(',')}` : '';
  const printUrl = `${frontendUrl}/print/analysis/${analysisId}?locale=${locale}${sectionsParam}`;
  
  logger.info(`📸 Screenshot PDF: Opening ${printUrl}`);
  
  const browser = await puppeteer.launch({
    headless: true,
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-dev-shm-usage',
      '--disable-gpu',
      '--font-render-hinting=none',
    ],
  });
  
  try {
    const page = await browser.newPage();

    page.on('console', (msg) => {
      if (msg.type() === 'error') {
        logger.warn(`Frontend console error: ${msg.text()}`);
      }
    });

    page.on('pageerror', (err) => {
      logger.warn(`Frontend page error: ${err.message}`);
    });
    
    // A4 boyutunda viewport
    await page.setViewport({
      width: 794,  // A4 width at 96 DPI
      height: 1123, // A4 height at 96 DPI
      deviceScaleFactor: 2, // Yüksek çözünürlük
    });
    
    // Sayfaya git ve yüklenmesini bekle
    await page.goto(printUrl, {
      waitUntil: 'networkidle0',
      timeout: 60000,
    });

    // Print CSS kurallarının tutarlı uygulanması için
    await page.emulateMediaType('print');

    // Ana container'ın gelmesini bekle
    await page.waitForSelector('#print-container', { timeout: 20000 });
    
    // Print ready sinyalini bekle (max 30 saniye)
    await page.waitForFunction(
      () => (window as any).__PRINT_READY__ === true,
      { timeout: 30000 }
    ).catch(() => {
      logger.warn('Print ready signal not received, continuing anyway...');
    });

    // Fontlar ve görseller tamamen yüklensin
    await page.waitForFunction(
      async () => {
        const fontsReady = (document as any).fonts ? await (document as any).fonts.ready.then(() => true).catch(() => false) : true;
        const imagesReady = Array.from(document.images || []).every((img) => img.complete);
        return fontsReady && imagesReady;
      },
      { timeout: 20000 }
    ).catch(() => {
      logger.warn('Fonts/images readiness timeout, continuing with current render state...');
    });
    
    // Ekstra bekleme - chartların tam render olması için
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // PDF oluştur
    const pdfBuffer = await page.pdf({
      format: 'A4',
      printBackground: true,
      margin: {
        top: '10mm',
        right: '10mm',
        bottom: '10mm',
        left: '10mm',
      },
      preferCSSPageSize: true,
    });
    
    logger.info(`✅ Screenshot PDF generated: ${pdfBuffer.length} bytes`);
    return Buffer.from(pdfBuffer);
    
  } finally {
    await browser.close();
  }
}

// Flexible recommendation schema - accepts string or any object format
const recommendationSchema = z.union([
  z.string(),
  z.object({
    text: z.string().optional(),
    recommendation: z.string().optional(),
    description: z.string().optional(),
    priority: z.union([z.string(), z.number()]).optional(),
    category: z.string().optional(),
    action: z.string().optional(),
    title: z.string().optional(),
    impact: z.string().optional(),
  }).passthrough().transform(obj => 
    obj.text || obj.recommendation || obj.description || obj.action || obj.title || JSON.stringify(obj)
  ),
]);

const payloadSchema = z.object({
  reportId: z.string().min(1),
  analysisId: z.string().min(1),
  accountData: z.object({
    username: z.string().min(1),
    followers: z.number().optional(),
    following: z.number().optional(),
    engagementRate: z.number().optional(),
    posts: z.number().optional(),
    bio: z.string().optional(),
    profilePicUrl: z.string().optional(),
    avgLikes: z.number().optional(),
    avgComments: z.number().optional(),
    botScore: z.number().optional(),
    isVerified: z.boolean().optional(),
  }),
  agentResults: z.record(z.any()).optional(),
  eli5Report: z.any().optional(),
  finalVerdict: z.any().optional(),
  businessIdentity: z.any().optional(),
  advancedAnalysis: z.any().optional(),
  contentPlan: z.any().optional(),
  overallScore: z.number().nullable().optional(),
  scoreGrade: z.string().nullable().optional(),
  recommendations: z.array(recommendationSchema).optional(),
  tier: z.string().optional(),
  // Custom PDF sections - kullanıcı hangi bölümleri dahil etmek istediğini seçebilir
  customSections: z.array(z.string()).optional(),
});

async function bootstrap() {
  await fs.mkdir(config.storageDir, { recursive: true }).catch(() => undefined);

  const app = express();
  app.use(cors());
  app.use(express.json({ limit: '2mb' }));
  app.use('/reports', express.static(config.storageDir));

  app.get('/health', (_req, res) => {
    res.json({ status: 'ok', service: 'pdf-generator' });
  });

  app.post('/generate', async (req, res, next) => {
    try {
      const payload = payloadSchema.parse(req.body);
      
      // Generate PDF using modern HTML/CSS system
      const buffer = await generatePDF(payload);
      
      // Save to storage
      const saveResult = await savePdf(payload.reportId, buffer);

      res.json({
        pdfUrl: saveResult.pdfUrl,
        s3Key: saveResult.s3Key,
        fileSize: buffer.length,
        pageCount: Math.ceil(buffer.length / 50000), // Estimate
      });
    } catch (error) {
      next(error);
    }
  });

  // 🆕 Screenshot-based PDF generation - Frontend chartlarını birebir yakalar
  app.post('/generate-screenshot', async (req, res, next) => {
    try {
      const { reportId, analysisId, sections, locale } = req.body;
      
      if (!reportId || !analysisId) {
        return res.status(400).json({ message: 'reportId and analysisId are required' });
      }
      
      logger.info(`📸 Generating screenshot PDF for analysis: ${analysisId}`);
      
      // Screenshot-based PDF oluştur
      const buffer = await generateScreenshotPDF(analysisId, sections, locale || 'tr');
      
      // Save to storage
      const saveResult = await savePdf(reportId, buffer);

      res.json({
        pdfUrl: saveResult.pdfUrl,
        s3Key: saveResult.s3Key,
        fileSize: buffer.length,
        pageCount: Math.ceil(buffer.length / 50000),
        method: 'screenshot',
      });
    } catch (error) {
      logger.error(error, 'Screenshot PDF generation failed');
      next(error);
    }
  });

  app.use((err: any, _req: express.Request, res: express.Response, _next: express.NextFunction) => {
    logger.error(err, 'PDF generator error');
    if (err instanceof z.ZodError) {
      return res.status(400).json({ message: 'Invalid payload', issues: err.flatten() });
    }
    return res.status(500).json({ message: 'Unable to generate PDF' });
  });

  app.listen(config.port, () => {
    logger.info(`PDF generator running on port ${config.port}`);
    logger.info(`Serving local PDFs from ${path.resolve(config.storageDir)}`);
    logger.info(`🎨 Using Modern HTML/CSS Template System (Puppeteer + Handlebars)`);
  });

  // Graceful shutdown
  process.on('SIGTERM', async () => {
    logger.info('SIGTERM received, cleaning up...');
    await cleanupGenerator();
    process.exit(0);
  });
}

bootstrap().catch((error) => {
  logger.error(error, 'Failed to start PDF generator');
  process.exit(1);
});
