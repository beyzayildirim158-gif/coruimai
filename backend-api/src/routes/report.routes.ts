// Report Routes
import { Router } from 'express';
import axios from 'axios';
import { prisma } from '../config/database.js';
import { config, tierLimits } from '../config/index.js';
import { authenticate } from '../middleware/auth.js';
import { asyncHandler } from '../utils/asyncHandler.js';
import { NotFoundError, ForbiddenError, BadRequestError } from '../utils/errors.js';
import { logger } from '../utils/logger.js';

const router = Router();

/**
 * @swagger
 * /api/reports/generate:
 *   post:
 *     summary: Generate PDF report for analysis
 *     tags: [Reports]
 *     security:
 *       - bearerAuth: []
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required: [analysisId]
 *             properties:
 *               analysisId:
 *                 type: string
 *               reportType:
 *                 type: string
 *                 enum: [FULL, SUMMARY, EXECUTIVE]
 *                 default: FULL
 *     responses:
 *       201:
 *         description: Report generation started
 */
router.post(
  '/generate',
  authenticate,
  asyncHandler(async (req, res) => {
    const { analysisId, reportType = 'FULL' } = req.body;
    const userId = req.user!.id;
    const tier = req.user!.subscriptionTier;

    // Check if analysis exists and belongs to user
    const analysis = await prisma.analysis.findFirst({
      where: {
        id: analysisId,
        userId,
        status: 'COMPLETED',
      },
      include: {
        account: true,
      },
    });

    if (!analysis) {
      throw new NotFoundError('Completed analysis not found');
    }

    // Check tier features
    const tierFeatures = tierLimits[tier as keyof typeof tierLimits].features;
    if (!tierFeatures.pdfReports) {
      throw new ForbiddenError('PDF reports not available in your plan');
    }

    // Check if report already exists
    const existingReport = await prisma.report.findFirst({
      where: {
        analysisId,
        reportType: reportType as any,
      },
    });

    if (existingReport?.pdfUrl) {
      return res.json({
        success: true,
        data: existingReport,
      });
    }

    // Create report record
    const report = await prisma.report.create({
      data: {
        userId,
        analysisId,
        reportType: reportType as any,
        isWatermarked: !tierFeatures.whiteLabelReports,
      },
    });

    // 🆕 Screenshot-based PDF - Frontend chartlarını birebir yakalar
    generateScreenshotPdfReport(report.id, analysisId, undefined, 'tr').catch((error) => {
      logger.error(`Screenshot PDF generation failed for report ${report.id}:`, error);
    });

    res.status(201).json({
      success: true,
      data: {
        reportId: report.id,
        status: 'GENERATING',
        message: 'Report generation started',
      },
    });
  })
);

/**
 * @swagger
 * /api/reports/generate-custom:
 *   post:
 *     summary: Generate customized PDF report with selected sections
 *     tags: [Reports]
 *     security:
 *       - bearerAuth: []
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required: [analysisId, sections]
 *             properties:
 *               analysisId:
 *                 type: string
 *               sections:
 *                 type: array
 *                 items:
 *                   type: string
 *                 description: Array of section IDs to include in the PDF
 *     responses:
 *       201:
 *         description: Custom report generation started
 */
router.post(
  '/generate-custom',
  authenticate,
  asyncHandler(async (req, res) => {
    const { analysisId, sections } = req.body;
    const userId = req.user!.id;
    const tier = req.user!.subscriptionTier;

    if (!sections || !Array.isArray(sections) || sections.length === 0) {
      throw new BadRequestError('At least one section must be selected');
    }

    // Check if analysis exists and belongs to user
    const analysis = await prisma.analysis.findFirst({
      where: {
        id: analysisId,
        userId,
        status: 'COMPLETED',
      },
      include: {
        account: true,
      },
    });

    if (!analysis) {
      throw new NotFoundError('Completed analysis not found');
    }

    // Check tier features
    const tierFeatures = tierLimits[tier as keyof typeof tierLimits].features;
    if (!tierFeatures.pdfReports) {
      throw new ForbiddenError('PDF reports not available in your plan');
    }

    // Validate section permissions based on tier
    const premiumSections = ['benchmarks', 'contentCalendar'];
    const standardSections = ['salesConversion', 'swotAnalysis', 'contentStrategy', 'hookRewrites'];
    
    // Map tier to access level
    const isPremiumTier = tier === 'PREMIUM' || tier === 'ENTERPRISE';
    const isStandardOrAbove = isPremiumTier || tier === 'PROFESSIONAL';
    
    for (const section of sections) {
      if (premiumSections.includes(section) && !isPremiumTier) {
        throw new ForbiddenError(`Section "${section}" requires premium tier`);
      }
      if (standardSections.includes(section) && !isStandardOrAbove) {
        throw new ForbiddenError(`Section "${section}" requires standard or premium tier`);
      }
    }

    // Create report record with CUSTOM type
    const report = await prisma.report.create({
      data: {
        userId,
        analysisId,
        reportType: 'CUSTOM' as any,
        isWatermarked: !tierFeatures.whiteLabelReports,
      },
    });

    // 🆕 Screenshot-based PDF - Frontend chartlarını birebir yakalar
    generateScreenshotPdfReport(report.id, analysisId, sections, 'tr').catch((error) => {
      logger.error(`Screenshot PDF generation failed for report ${report.id}:`, error);
    });

    res.status(201).json({
      success: true,
      data: {
        reportId: report.id,
        status: 'GENERATING',
        message: 'Custom report generation started',
        sections,
      },
    });
  })
);

/**
 * @swagger
 * /api/reports/{id}:
 *   get:
 *     summary: Get report details
 *     tags: [Reports]
 *     security:
 *       - bearerAuth: []
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: string
 *     responses:
 *       200:
 *         description: Report details
 */
router.get(
  '/:id',
  authenticate,
  asyncHandler(async (req, res) => {
    const { id } = req.params;
    const userId = req.user!.id;

    const report = await prisma.report.findFirst({
      where: {
        id,
        userId,
      },
      include: {
        analysis: {
          include: {
            account: {
              select: {
                username: true,
                profilePicUrl: true,
              },
            },
          },
        },
      },
    });

    if (!report) {
      throw new NotFoundError('Report not found');
    }

    res.json({
      success: true,
      data: report,
    });
  })
);

/**
 * @swagger
 * /api/reports/{id}/download:
 *   get:
 *     summary: Download report PDF
 *     tags: [Reports]
 *     security:
 *       - bearerAuth: []
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: string
 *     responses:
 *       302:
 *         description: Redirect to PDF URL
 */
router.get(
  '/:id/download',
  authenticate,
  asyncHandler(async (req, res) => {
    const { id } = req.params;
    const userId = req.user!.id;

    const report = await prisma.report.findFirst({
      where: {
        id,
        userId,
      },
    });

    if (!report) {
      throw new NotFoundError('Report not found');
    }

    if (!report.pdfUrl) {
      throw new BadRequestError('Report is still being generated');
    }

    // Redirect to PDF URL
    res.redirect(report.pdfUrl);
  })
);

/**
 * @swagger
 * /api/reports:
 *   get:
 *     summary: List user's reports
 *     tags: [Reports]
 *     security:
 *       - bearerAuth: []
 *     responses:
 *       200:
 *         description: List of reports
 */
router.get(
  '/',
  authenticate,
  asyncHandler(async (req, res) => {
    const userId = req.user!.id;
    const page = Math.max(1, parseInt(req.query.page as string) || 1);
    const limit = Math.min(50, parseInt(req.query.limit as string) || 10);
    const skip = (page - 1) * limit;

    const [reports, total] = await Promise.all([
      prisma.report.findMany({
        where: { userId },
        skip,
        take: limit,
        orderBy: { createdAt: 'desc' },
        include: {
          analysis: {
            include: {
              account: {
                select: {
                  username: true,
                  profilePicUrl: true,
                },
              },
            },
          },
        },
      }),
      prisma.report.count({ where: { userId } }),
    ]);

    res.json({
      success: true,
      data: {
        reports,
        pagination: {
          page,
          limit,
          total,
          totalPages: Math.ceil(total / limit),
        },
      },
    });
  })
);

// Helper function to generate PDF
async function generatePdfReport(
  reportId: string,
  analysis: any,
  tier: string
): Promise<void> {
  try {
    // Extract special sections from agentResults
    const {
      eli5Report,
      finalVerdict,
      businessIdentity,
      advancedAnalysis,
      contentPlan,
      sanitizationReport,
      hardValidation,
      ...otherAgentResults
    } = analysis.agentResults || {};

    const response = await axios.post(
      `${config.pdfGenerator.url}/generate`,
      {
        reportId,
        analysisId: analysis.id,
        accountData: {
          ...analysis.account,
          // Include account data from InstagramAccount model
          botScore: analysis.account?.botScore,
          avgLikes: analysis.account?.avgLikes,
          avgComments: analysis.account?.avgComments,
        },
        agentResults: otherAgentResults,
        eli5Report,
        finalVerdict,
        businessIdentity,
        advancedAnalysis,
        contentPlan,
        sanitizationReport,
        hardValidation,
        overallScore: analysis.overallScore,
        scoreGrade: analysis.scoreGrade,
        recommendations: analysis.recommendations,
        tier,
      },
      {
        timeout: 120000, // 2 minute timeout for larger PDFs
      }
    );

    // Update report with PDF URL
    await prisma.report.update({
      where: { id: reportId },
      data: {
        pdfUrl: response.data.pdfUrl,
        s3Key: response.data.s3Key,
        fileSize: response.data.fileSize,
        pageCount: response.data.pageCount,
        generatedAt: new Date(),
      },
    });

    logger.info(`PDF generated for report ${reportId}`);
  } catch (error) {
    logger.error(`PDF generation failed for report ${reportId}:`, error);
    throw error;
  }
}

// Helper function to generate custom PDF with selected sections
async function generateCustomPdfReport(
  reportId: string,
  analysis: any,
  tier: string,
  sections: string[]
): Promise<void> {
  try {
    // Extract special sections from agentResults
    const {
      eli5Report,
      finalVerdict,
      businessIdentity,
      advancedAnalysis,
      contentPlan,
      sanitizationReport,
      hardValidation,
      ...otherAgentResults
    } = analysis.agentResults || {};

    // Filter agent results based on selected sections
    const filteredAgentResults: Record<string, any> = {};
    const agentSectionMap: Record<string, string> = {
      domainMaster: 'domainMaster',
      growthVirality: 'growthVirality',
      salesConversion: 'salesConversion',
      visualBrand: 'visualBrand',
      communityLoyalty: 'communityLoyalty',
      attentionArchitect: 'attentionArchitect',
      systemGovernor: 'systemGovernor',
    };

    for (const [agentKey, sectionId] of Object.entries(agentSectionMap)) {
      if (sections.includes(sectionId) && otherAgentResults[agentKey]) {
        filteredAgentResults[agentKey] = otherAgentResults[agentKey];
      }
    }

    const response = await axios.post(
      `${config.pdfGenerator.url}/generate`,
      {
        reportId,
        analysisId: analysis.id,
        accountData: {
          ...analysis.account,
          botScore: analysis.account?.botScore,
          avgLikes: analysis.account?.avgLikes,
          avgComments: analysis.account?.avgComments,
        },
        // Pass filtered agent results
        agentResults: filteredAgentResults,
        // Conditionally include special sections
        eli5Report: sections.includes('eli5Report') ? eli5Report : undefined,
        finalVerdict: sections.includes('finalVerdict') ? finalVerdict : undefined,
        businessIdentity: sections.includes('businessIdentity') ? businessIdentity : undefined,
        advancedAnalysis: sections.includes('contentStrategy') || sections.includes('actionPlan') || sections.includes('riskAssessment') 
          ? advancedAnalysis : undefined,
        contentPlan: sections.includes('contentCalendar') ? contentPlan : undefined,
        sanitizationReport: sanitizationReport,
        hardValidation: hardValidation,
        overallScore: analysis.overallScore,
        scoreGrade: analysis.scoreGrade,
        recommendations: analysis.recommendations,
        tier,
        // Pass custom sections configuration
        customSections: sections,
      },
      {
        timeout: 120000,
      }
    );

    // Update report with PDF URL
    await prisma.report.update({
      where: { id: reportId },
      data: {
        pdfUrl: response.data.pdfUrl,
        s3Key: response.data.s3Key,
        fileSize: response.data.fileSize,
        pageCount: response.data.pageCount,
        generatedAt: new Date(),
      },
    });

    logger.info(`Custom PDF generated for report ${reportId} with sections: ${sections.join(', ')}`);
  } catch (error) {
    logger.error(`Custom PDF generation failed for report ${reportId}:`, error);
    throw error;
  }
}

// 🆕 Screenshot-based PDF generation - Frontend'i birebir yakalar
async function generateScreenshotPdfReport(
  reportId: string,
  analysisId: string,
  sections?: string[],
  locale: string = 'tr'
): Promise<void> {
  try {
    logger.info(`📸 Starting screenshot PDF generation for report ${reportId}`);
    
    const response = await axios.post(
      `${config.pdfGenerator.url}/generate-screenshot`,
      {
        reportId,
        analysisId,
        sections,
        locale,
      },
      {
        timeout: 120000,
      }
    );

    // Update report with PDF URL
    await prisma.report.update({
      where: { id: reportId },
      data: {
        pdfUrl: response.data.pdfUrl,
        s3Key: response.data.s3Key,
        fileSize: response.data.fileSize,
        pageCount: response.data.pageCount,
        generatedAt: new Date(),
      },
    });

    logger.info(`📸 Screenshot PDF generated for report ${reportId}`);
  } catch (error) {
    logger.error(`Screenshot PDF generation failed for report ${reportId}:`, error);
    throw error;
  }
}

export default router;
