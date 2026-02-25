// Analysis Routes
import { Router } from 'express';
import { z } from 'zod';
import axios from 'axios';
import { prisma } from '../config/database.js';
import { config, tierLimits } from '../config/index.js';
import { authenticate, requireEmailVerified } from '../middleware/auth.js';
import { tierRateLimiter, analysisLimiter, incrementAnalysisUsage } from '../middleware/rateLimiter.js';
import { validateRequest } from '../middleware/validate.js';
import { asyncHandler } from '../utils/asyncHandler.js';
import { instagramDataService } from '../services/instagram.service.js';
import { NotFoundError, ForbiddenError, BadRequestError } from '../utils/errors.js';
import { logger } from '../utils/logger.js';
import { broadcastAnalysisUpdate } from '../websocket/index.js';

const router = Router();

// Validation schemas
const startAnalysisSchema = z.object({
  body: z.object({
    username: z.string().min(1, 'Username is required').max(30),
    // Instagram login credentials for authenticated scraping
    instagramCredentials: z.object({
      username: z.string().min(1),
      password: z.string().min(1),
    }).optional(),
    // Analysis mode: 'public' for public data only, 'authenticated' for login scrape
    mode: z.enum(['public', 'authenticated']).optional().default('public'),
  }),
});

/**
 * @swagger
 * /api/analyze/start:
 *   post:
 *     summary: Start Instagram account analysis
 *     tags: [Analysis]
 *     security:
 *       - bearerAuth: []
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required: [username]
 *             properties:
 *               username:
 *                 type: string
 *                 example: instagram
 *     responses:
 *       201:
 *         description: Analysis started
 *       400:
 *         description: Invalid username
 *       403:
 *         description: Analysis limit reached
 *       429:
 *         description: Rate limit exceeded
 */
router.post(
  '/start',
  authenticate,
  requireEmailVerified,
  tierRateLimiter,
  analysisLimiter,
  validateRequest(startAnalysisSchema),
  asyncHandler(async (req, res) => {
    const { username, instagramCredentials, mode } = req.body;
    const userId = req.user!.id;
    const tier = req.user!.subscriptionTier;

    // Normalize username
    const normalizedUsername = username.replace(/^@/, '').trim().toLowerCase();

    // Validate username format
    if (!/^[a-z0-9._]{1,30}$/.test(normalizedUsername)) {
      throw new BadRequestError('Invalid Instagram username format');
    }

    // Fetch Instagram data
    logger.info(`Starting analysis for @${normalizedUsername} by user ${userId}`);
    const accountData = await instagramDataService.fetchAccountData(normalizedUsername);

    // Check if account is private
    if (accountData.isPrivate) {
      throw new BadRequestError('Cannot analyze private accounts');
    }

    // Create or update Instagram account
    const instagramAccount = await prisma.instagramAccount.upsert({
      where: {
        userId_username: {
          userId,
          username: normalizedUsername,
        },
      },
      create: {
        userId,
        username: normalizedUsername,
        followers: accountData.followers,
        following: accountData.following,
        posts: accountData.posts,
        bio: accountData.bio,
        profilePicUrl: accountData.profilePicUrl,
        profilePicData: accountData.profilePicBase64,
        isVerified: accountData.verified,
        isPrivate: accountData.isPrivate,
        isBusiness: accountData.isBusiness,
        engagementRate: accountData.engagementRate,
        avgLikes: accountData.avgLikes,
        avgComments: accountData.avgComments,
        botScore: accountData.botScore,
        accountData: accountData.rawData,
      },
      update: {
        followers: accountData.followers,
        following: accountData.following,
        posts: accountData.posts,
        bio: accountData.bio,
        profilePicUrl: accountData.profilePicUrl,
        profilePicData: accountData.profilePicBase64,
        isVerified: accountData.verified,
        isBusiness: accountData.isBusiness,
        engagementRate: accountData.engagementRate,
        avgLikes: accountData.avgLikes,
        avgComments: accountData.avgComments,
        botScore: accountData.botScore,
        accountData: accountData.rawData,
      },
    });

    // Create analysis record
    const analysis = await prisma.analysis.create({
      data: {
        userId,
        accountId: instagramAccount.id,
        status: 'PENDING',
        progress: 0,
      },
    });

    // Get available agents for tier
    const availableAgents = [...tierLimits[tier as keyof typeof tierLimits].agents] as string[];

    // Start agent orchestrator (async)
    startAgentAnalysis(analysis.id, accountData, availableAgents, mode, instagramCredentials).catch((error) => {
      logger.error(`Agent analysis failed for ${analysis.id}:`, error);
    });

    // Increment usage
    await incrementAnalysisUsage(userId);

    res.status(201).json({
      success: true,
      data: {
        analysisId: analysis.id,
        account: {
          username: accountData.username,
          followers: accountData.followers,
          following: accountData.following,
          posts: accountData.posts,
          engagementRate: accountData.engagementRate,
          profilePicUrl: accountData.profilePicUrl,
        },
        status: 'PENDING',
        agents: availableAgents,
      },
    });
  })
);

/**
 * @swagger
 * /api/analyze/status/{id}:
 *   get:
 *     summary: Get analysis status
 *     tags: [Analysis]
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
 *         description: Analysis status
 *       404:
 *         description: Analysis not found
 */
router.get(
  '/status/:id',
  authenticate,
  asyncHandler(async (req, res) => {
    const { id } = req.params;
    const userId = req.user!.id;

    const analysis = await prisma.analysis.findFirst({
      where: {
        id,
        userId,
      },
      select: {
        id: true,
        status: true,
        progress: true,
        currentAgent: true,
        errorMessage: true,
        startedAt: true,
        completedAt: true,
        createdAt: true,
        account: {
          select: {
            username: true,
            profilePicUrl: true,
            profilePicData: true,
          },
        },
      },
    });

    if (!analysis) {
      throw new NotFoundError('Analysis not found');
    }

    // Use base64 data if available, otherwise use CDN URL
    const accountWithPic = {
      ...analysis.account,
      profilePicUrl: analysis.account.profilePicData || analysis.account.profilePicUrl,
    };

    res.json({
      success: true,
      data: {
        ...analysis,
        account: accountWithPic,
      },
    });
  })
);

/**
 * @swagger
 * /api/analyze/result/{id}:
 *   get:
 *     summary: Get analysis results
 *     tags: [Analysis]
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
 *         description: Analysis results
 *       404:
 *         description: Analysis not found
 */
router.get(
  '/result/:id',
  authenticate,
  asyncHandler(async (req, res) => {
    const { id } = req.params;
    const userId = req.user!.id;

    const analysis = await prisma.analysis.findFirst({
      where: {
        id,
        userId,
      },
      include: {
        account: {
          select: {
            username: true,
            followers: true,
            following: true,
            posts: true,
            bio: true,
            profilePicUrl: true,
            profilePicData: true,
            isVerified: true,
            isBusiness: true,
            engagementRate: true,
            avgLikes: true,
            avgComments: true,
            botScore: true,
            accountData: true,
          },
        },
        reports: {
          select: {
            id: true,
            pdfUrl: true,
            reportType: true,
            generatedAt: true,
          },
        },
      },
    });

    if (!analysis) {
      throw new NotFoundError('Analysis not found');
    }

    if (analysis.status !== 'COMPLETED') {
      throw new BadRequestError(`Analysis is ${analysis.status.toLowerCase()}`);
    }

    // Use base64 data if available, otherwise use CDN URL
    const accountWithPic = {
      ...analysis.account,
      profilePicUrl: analysis.account.profilePicData || analysis.account.profilePicUrl,
    };

    res.json({
      success: true,
      data: {
        ...analysis,
        account: accountWithPic,
      },
    });
  })
);

/**
 * @swagger
 * /api/analyze/print/{id}:
 *   get:
 *     summary: Get analysis results for PDF print (no auth required - internal use only)
 *     tags: [Analysis]
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: string
 *     responses:
 *       200:
 *         description: Analysis results
 *       404:
 *         description: Analysis not found
 */
router.get(
  '/print/:id',
  asyncHandler(async (req, res) => {
    const { id } = req.params;

    // Bu endpoint sadece internal kullanım içindir (PDF generator)
    // Production'da IP kısıtlaması eklenebilir
    const analysis = await prisma.analysis.findFirst({
      where: {
        id,
        status: 'COMPLETED',
      },
      include: {
        account: {
          select: {
            username: true,
            followers: true,
            following: true,
            posts: true,
            bio: true,
            profilePicUrl: true,
            profilePicData: true,
            isVerified: true,
            isBusiness: true,
            engagementRate: true,
            avgLikes: true,
            avgComments: true,
            botScore: true,
            accountData: true,
          },
        },
      },
    });

    if (!analysis) {
      throw new NotFoundError('Analysis not found');
    }

    // Use base64 data if available, otherwise use CDN URL
    const accountWithPic = {
      ...analysis.account,
      profilePicUrl: analysis.account.profilePicData || analysis.account.profilePicUrl,
    };

    res.json({
      success: true,
      data: {
        ...analysis,
        account: accountWithPic,
      },
    });
  })
);

/**
 * @swagger
 * /api/analyze/cancel/{id}:
 *   post:
 *     summary: Cancel running analysis
 *     tags: [Analysis]
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
 *         description: Analysis cancelled
 */
router.post(
  '/cancel/:id',
  authenticate,
  asyncHandler(async (req, res) => {
    const { id } = req.params;
    const userId = req.user!.id;

    const analysis = await prisma.analysis.findFirst({
      where: {
        id,
        userId,
        status: { in: ['PENDING', 'PROCESSING'] },
      },
    });

    if (!analysis) {
      throw new NotFoundError('Analysis not found or already completed');
    }

    // Cancel in orchestrator
    try {
      await axios.post(`${config.agentOrchestrator.url}/analyze/cancel/${id}`);
    } catch (error) {
      logger.warn(`Failed to cancel analysis in orchestrator: ${id}`);
    }

    // Update status
    await prisma.analysis.update({
      where: { id },
      data: { status: 'CANCELLED' },
    });

    res.json({
      success: true,
      message: 'Analysis cancelled',
    });
  })
);

/**
 * @swagger
 * /api/analyze/history:
 *   get:
 *     summary: Get recent analyses
 *     tags: [Analysis]
 *     security:
 *       - bearerAuth: []
 *     responses:
 *       200:
 *         description: Recent analyses
 */
router.get(
  '/history',
  authenticate,
  asyncHandler(async (req, res) => {
    const userId = req.user!.id;
    const limit = Math.min(20, parseInt(req.query.limit as string) || 10);

    const analyses = await prisma.analysis.findMany({
      where: { userId },
      take: limit,
      orderBy: { createdAt: 'desc' },
      select: {
        id: true,
        status: true,
        overallScore: true,
        scoreGrade: true,
        createdAt: true,
        completedAt: true,
        account: {
          select: {
            username: true,
            profilePicUrl: true,
            followers: true,
          },
        },
      },
    });

    res.json({
      success: true,
      data: analyses,
    });
  })
);

// ==============================================================
// CONTENT PLAN GENERATION ENDPOINTS
// ==============================================================

/**
 * @swagger
 * /api/analyze/{analysisId}/content-plan:
 *   post:
 *     summary: Generate a 7-day content plan from completed analysis
 *     tags: [Analysis, Content Plan]
 *     security:
 *       - bearerAuth: []
 *     parameters:
 *       - in: path
 *         name: analysisId
 *         required: true
 *         schema:
 *           type: string
 *     responses:
 *       200:
 *         description: Content plan generated successfully
 *       400:
 *         description: Analysis not completed or insufficient data
 *       404:
 *         description: Analysis not found
 */
router.post(
  '/:analysisId/content-plan',
  authenticate,
  requireEmailVerified,
  asyncHandler(async (req, res) => {
    const { analysisId } = req.params;
    const userId = req.user!.id;

    // Verify analysis exists and belongs to user
    const analysis = await prisma.analysis.findFirst({
      where: {
        id: analysisId,
        account: { userId },
      },
      include: {
        account: true,
      },
    });

    if (!analysis) {
      throw new NotFoundError('Analysis not found');
    }

    if (analysis.status !== 'COMPLETED') {
      throw new BadRequestError(
        `Analysis must be completed first. Current status: ${analysis.status}`
      );
    }

    logger.info(`Generating content plan for analysis ${analysisId}`);

    try {
      // Call agent orchestrator to generate content plan
      const response = await axios.post(
        `${config.agentOrchestrator.url}/content-plan/from-analysis/${analysisId}`,
        {},
        {
          timeout: 120000, // 2 minute timeout for content plan generation
        }
      );

      if (!response.data.success) {
        throw new BadRequestError(
          response.data.error || 'Failed to generate content plan'
        );
      }

      // Store content plan reference in database
      await prisma.analysis.update({
        where: { id: analysisId },
        data: {
          // Add hasContentPlan flag or store the plan
          // For now we'll rely on Redis storage in orchestrator
        },
      });

      res.json({
        success: true,
        analysisId,
        contentPlan: response.data.contentPlan,
        metadata: response.data.metadata,
      });
    } catch (error: any) {
      logger.error(`Content plan generation failed for ${analysisId}:`, error);
      
      if (error.response?.data) {
        throw new BadRequestError(
          error.response.data.detail || 'Content plan generation failed'
        );
      }
      throw error;
    }
  })
);

/**
 * @swagger
 * /api/analyze/{analysisId}/content-plan:
 *   get:
 *     summary: Get a previously generated content plan
 *     tags: [Analysis, Content Plan]
 *     security:
 *       - bearerAuth: []
 *     parameters:
 *       - in: path
 *         name: analysisId
 *         required: true
 *         schema:
 *           type: string
 *     responses:
 *       200:
 *         description: Content plan retrieved successfully
 *       404:
 *         description: Content plan not found
 */
router.get(
  '/:analysisId/content-plan',
  authenticate,
  requireEmailVerified,
  asyncHandler(async (req, res) => {
    const { analysisId } = req.params;
    const userId = req.user!.id;

    // Verify analysis exists and belongs to user
    const analysis = await prisma.analysis.findFirst({
      where: {
        id: analysisId,
        account: { userId },
      },
    });

    if (!analysis) {
      throw new NotFoundError('Analysis not found');
    }

    try {
      // Get content plan from orchestrator
      const response = await axios.get(
        `${config.agentOrchestrator.url}/content-plan/${analysisId}`,
        {
          timeout: 30000,
        }
      );

      res.json({
        success: true,
        analysisId,
        contentPlan: response.data.contentPlan,
      });
    } catch (error: any) {
      if (error.response?.status === 404) {
        throw new NotFoundError(
          'Content plan not found. Generate one first using POST /api/analyze/{analysisId}/content-plan'
        );
      }
      throw error;
    }
  })
);

/**
 * @swagger
 * /api/analyze/{analysisId}/content-plan/validate:
 *   get:
 *     summary: Validate if analysis has sufficient data for content plan
 *     tags: [Analysis, Content Plan]
 *     security:
 *       - bearerAuth: []
 *     parameters:
 *       - in: path
 *         name: analysisId
 *         required: true
 *         schema:
 *           type: string
 *     responses:
 *       200:
 *         description: Validation result
 */
router.get(
  '/:analysisId/content-plan/validate',
  authenticate,
  requireEmailVerified,
  asyncHandler(async (req, res) => {
    const { analysisId } = req.params;
    const userId = req.user!.id;

    // Verify analysis exists and belongs to user
    const analysis = await prisma.analysis.findFirst({
      where: {
        id: analysisId,
        account: { userId },
      },
    });

    if (!analysis) {
      throw new NotFoundError('Analysis not found');
    }

    try {
      const response = await axios.post(
        `${config.agentOrchestrator.url}/content-plan/validate-data/${analysisId}`,
        {},
        {
          timeout: 30000,
        }
      );

      res.json({
        success: true,
        analysisId,
        validation: response.data.validation,
        canGeneratePlan: response.data.canGeneratePlan,
      });
    } catch (error: any) {
      if (error.response?.status === 404) {
        throw new NotFoundError('Analysis results not found');
      }
      throw error;
    }
  })
);

/**
 * @swagger
 * /api/analyze/{analysisId}/content-plan:
 *   delete:
 *     summary: Delete a generated content plan
 *     tags: [Analysis, Content Plan]
 *     security:
 *       - bearerAuth: []
 *     parameters:
 *       - in: path
 *         name: analysisId
 *         required: true
 *         schema:
 *           type: string
 *     responses:
 *       200:
 *         description: Content plan deleted
 */
router.delete(
  '/:analysisId/content-plan',
  authenticate,
  requireEmailVerified,
  asyncHandler(async (req, res) => {
    const { analysisId } = req.params;
    const userId = req.user!.id;

    // Verify analysis exists and belongs to user
    const analysis = await prisma.analysis.findFirst({
      where: {
        id: analysisId,
        account: { userId },
      },
    });

    if (!analysis) {
      throw new NotFoundError('Analysis not found');
    }

    try {
      const response = await axios.delete(
        `${config.agentOrchestrator.url}/content-plan/${analysisId}`,
        {
          timeout: 30000,
        }
      );

      res.json({
        success: response.data.success,
        message: response.data.message,
      });
    } catch (error: any) {
      throw error;
    }
  })
);

// ==============================================================
// END CONTENT PLAN GENERATION ENDPOINTS
// ==============================================================

// ==============================================================
// DELTA SYNC ENDPOINT - Get Previous Analysis for Comparison
// ==============================================================

/**
 * @swagger
 * /api/analyze/previous/{username}:
 *   get:
 *     summary: Get previous analysis for a username (Delta Sync)
 *     description: Internal endpoint used by agent orchestrator for comparing current analysis with previous results
 *     tags: [Analysis, Delta Sync]
 *     parameters:
 *       - in: path
 *         name: username
 *         required: true
 *         schema:
 *           type: string
 *     responses:
 *       200:
 *         description: Previous analysis found (or empty if none exists)
 *       500:
 *         description: Server error
 */
router.get(
  '/previous/:username',
  asyncHandler(async (req, res) => {
    const { username } = req.params;
    const normalizedUsername = username.replace(/^@/, '').trim().toLowerCase();

    logger.info(`Delta sync: Looking for previous analysis for @${normalizedUsername}`);

    try {
      // Find the most recent completed analysis for this username
      const previousAnalysis = await prisma.analysis.findFirst({
        where: {
          account: {
            username: normalizedUsername,
          },
          status: 'COMPLETED',
        },
        orderBy: {
          completedAt: 'desc',
        },
        include: {
          account: {
            select: {
              username: true,
              followers: true,
              following: true,
              posts: true,
              engagementRate: true,
            },
          },
        },
      });

      if (!previousAnalysis) {
        logger.info(`Delta sync: No previous analysis found for @${normalizedUsername}`);
        return res.json({
          success: true,
          analysis: null,
          message: 'No previous analysis found',
        });
      }

      // Parse the agentResults from JSON
      let agentResults = {};
      if (previousAnalysis.agentResults) {
        try {
          agentResults = typeof previousAnalysis.agentResults === 'string'
            ? JSON.parse(previousAnalysis.agentResults)
            : previousAnalysis.agentResults;
        } catch (e) {
          logger.warn(`Could not parse agentResults for analysis ${previousAnalysis.id}`);
        }
      }

      logger.info(`Delta sync: Found previous analysis from ${previousAnalysis.completedAt}`);

      res.json({
        success: true,
        analysis: {
          id: previousAnalysis.id,
          finalScore: previousAnalysis.overallScore,
          finalGrade: previousAnalysis.scoreGrade,
          analysisCompletedAt: previousAnalysis.completedAt?.toISOString(),
          account: previousAnalysis.account,
          agentResults,
        },
      });
    } catch (error) {
      logger.error(`Delta sync error for @${normalizedUsername}:`, error);
      res.json({
        success: false,
        analysis: null,
        error: 'Failed to fetch previous analysis',
      });
    }
  })
);

// ==============================================================
// END DELTA SYNC ENDPOINT
// ==============================================================

// Helper function to start agent analysis
async function startAgentAnalysis(
  analysisId: string,
  accountData: any,
  agents: string[],
  mode: string = 'public',
  credentials?: { username: string; password: string }
): Promise<void> {
  try {
    // Update status to processing
    await prisma.analysis.update({
      where: { id: analysisId },
      data: {
        status: 'PROCESSING',
        startedAt: new Date(),
        currentAgent: agents[0],
      },
    });

    // Broadcast initial update
    broadcastAnalysisUpdate(analysisId, {
      status: 'PROCESSING',
      progress: 0,
      currentAgent: agents[0],
    });

    // Prepare request payload
    const payload: any = {
      analysisId,
      accountData,
      agents,
      mode,
    };

    // Add own_account for authenticated mode with credentials
    if (mode === 'authenticated' && credentials) {
      payload.own_account = {
        username: credentials.username,
        password: credentials.password,
        fetch_private: true,
      };
    }

    // Call agent orchestrator
    const response = await axios.post(
      `${config.agentOrchestrator.url}/analyze/start`,
      payload,
      {
        timeout: config.agentOrchestrator.timeout * 1000,
      }
    );

    // Results will be updated via webhook from orchestrator
    logger.info(`Agent analysis started for ${analysisId}`);
  } catch (error) {
    logger.error(`Failed to start agent analysis for ${analysisId}:`, error);

    // Update analysis as failed
    await prisma.analysis.update({
      where: { id: analysisId },
      data: {
        status: 'FAILED',
        errorMessage: 'Failed to start AI analysis. Please try again.',
      },
    });

    broadcastAnalysisUpdate(analysisId, {
      status: 'FAILED',
      error: 'Failed to start AI analysis',
    });
  }
}

export default router;
