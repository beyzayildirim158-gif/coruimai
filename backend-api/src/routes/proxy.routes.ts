// Image Proxy Routes - Bypass CORS for external images
import { Router } from 'express';
import { asyncHandler } from '../utils/asyncHandler.js';

const router = Router();

// Handle CORS preflight for image proxy
router.options('/image', (req, res) => {
  res.set({
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '86400',
  });
  res.status(204).end();
});

/**
 * @swagger
 * /api/proxy/image:
 *   get:
 *     summary: Proxy external images to bypass CORS
 *     tags: [Proxy]
 *     parameters:
 *       - in: query
 *         name: url
 *         required: true
 *         schema:
 *           type: string
 *         description: The URL of the image to proxy
 *     responses:
 *       200:
 *         description: Image data
 *         content:
 *           image/*:
 *             schema:
 *               type: string
 *               format: binary
 *       400:
 *         description: Missing or invalid URL
 *       502:
 *         description: Failed to fetch image
 */
router.get(
  '/image',
  asyncHandler(async (req, res) => {
    const imageUrl = req.query.url as string;

    if (!imageUrl) {
      return res.status(400).json({ error: 'Missing url parameter' });
    }

    // Validate URL - only allow Instagram CDN domains
    const allowedDomains = [
      'instagram.com',
      'cdninstagram.com',
      'fbcdn.net',
      'scontent.cdninstagram.com',
    ];

    let url: URL;
    try {
      url = new URL(imageUrl);
    } catch {
      return res.status(400).json({ error: 'Invalid URL' });
    }

    const isAllowed = allowedDomains.some(domain => url.hostname.endsWith(domain));
    if (!isAllowed) {
      return res.status(403).json({ error: 'Domain not allowed' });
    }

    try {
      console.log('Proxying image:', imageUrl);
      const controller = new AbortController();
      const timeout = setTimeout(() => controller.abort(), 10000);
      
      const response = await fetch(imageUrl, {
        signal: controller.signal,
        headers: {
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
          'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
          'Accept-Language': 'en-US,en;q=0.9',
          'Referer': 'https://www.instagram.com/',
        },
      });
      
      clearTimeout(timeout);
      console.log('Image fetch response:', response.status, response.statusText);

      if (!response.ok) {
        console.log('Image fetch failed:', response.status, response.statusText);
        return res.status(502).json({ error: 'Failed to fetch image' });
      }

      const contentType = response.headers.get('content-type') || 'image/jpeg';
      const buffer = await response.arrayBuffer();

      // Cache for 1 hour and allow cross-origin access
      res.set({
        'Content-Type': contentType,
        'Cache-Control': 'public, max-age=3600',
        'Access-Control-Allow-Origin': '*',
        'Cross-Origin-Resource-Policy': 'cross-origin',
        'Cross-Origin-Embedder-Policy': 'unsafe-none',
      });

      res.send(Buffer.from(buffer));
    } catch (error) {
      console.error('Image proxy error:', error);
      return res.status(502).json({ error: 'Failed to fetch image' });
    }
  })
);

export default router;
