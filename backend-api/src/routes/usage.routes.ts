// Usage Routes
import { Router } from 'express';
import { prisma } from '../config/database.js';
import { tierLimits } from '../config/index.js';
import { authenticate } from '../middleware/auth.js';
import { getAnalysisUsage } from '../middleware/rateLimiter.js';
import { asyncHandler } from '../utils/asyncHandler.js';

const router = Router();

/**
 * @swagger
 * /api/usage/current:
 *   get:
 *     summary: Get current month usage
 *     tags: [Usage]
 *     security:
 *       - bearerAuth: []
 *     responses:
 *       200:
 *         description: Current usage statistics
 */
router.get(
  '/current',
  authenticate,
  asyncHandler(async (req, res) => {
    const userId = req.user!.id;
    const tier = req.user!.subscriptionTier;

    const analysisUsage = await getAnalysisUsage(userId);
    const tierConfig = tierLimits[tier as keyof typeof tierLimits];

    res.json({
      success: true,
      data: {
        analyses: {
          used: analysisUsage.used,
          limit: analysisUsage.limit,
          remaining: analysisUsage.remaining,
        },
        tier: {
          name: tier,
          requestsPerHour: tierConfig.requestsPerHour,
          agentCount: tierConfig.agentCount,
          features: tierConfig.features,
        },
      },
    });
  })
);

/**
 * @swagger
 * /api/usage/history:
 *   get:
 *     summary: Get usage history
 *     tags: [Usage]
 *     security:
 *       - bearerAuth: []
 *     parameters:
 *       - in: query
 *         name: months
 *         schema:
 *           type: integer
 *           default: 6
 *     responses:
 *       200:
 *         description: Usage history
 */
router.get(
  '/history',
  authenticate,
  asyncHandler(async (req, res) => {
    const userId = req.user!.id;
    const months = Math.min(12, parseInt(req.query.months as string) || 6);

    // Get last N months
    const startDate = new Date();
    startDate.setMonth(startDate.getMonth() - months);
    const startMonthYear = `${startDate.getFullYear()}-${String(startDate.getMonth() + 1).padStart(2, '0')}`;

    const usage = await prisma.apiUsage.findMany({
      where: {
        userId,
        monthYear: { gte: startMonthYear },
      },
      orderBy: { monthYear: 'asc' },
      select: {
        monthYear: true,
        analysesUsed: true,
        requestsCount: true,
      },
    });

    // Also get analysis counts per month
    const analyses = await prisma.analysis.groupBy({
      by: ['createdAt'],
      where: {
        userId,
        createdAt: { gte: startDate },
      },
      _count: true,
    });

    res.json({
      success: true,
      data: {
        usage,
        monthlyAnalyses: analyses,
      },
    });
  })
);

/**
 * @swagger
 * /api/usage/stats:
 *   get:
 *     summary: Get detailed usage stats
 *     tags: [Usage]
 *     security:
 *       - bearerAuth: []
 *     responses:
 *       200:
 *         description: Detailed statistics
 */
router.get(
  '/stats',
  authenticate,
  asyncHandler(async (req, res) => {
    const userId = req.user!.id;

    const [
      totalAnalyses,
      completedAnalyses,
      failedAnalyses,
      totalReports,
      accountsAnalyzed,
    ] = await Promise.all([
      prisma.analysis.count({ where: { userId } }),
      prisma.analysis.count({ where: { userId, status: 'COMPLETED' } }),
      prisma.analysis.count({ where: { userId, status: 'FAILED' } }),
      prisma.report.count({ where: { userId } }),
      prisma.instagramAccount.count({ where: { userId } }),
    ]);

    // Get average scores
    const avgScore = await prisma.analysis.aggregate({
      where: {
        userId,
        status: 'COMPLETED',
        overallScore: { not: null },
      },
      _avg: {
        overallScore: true,
      },
    });

    res.json({
      success: true,
      data: {
        totalAnalyses,
        completedAnalyses,
        failedAnalyses,
        successRate: totalAnalyses > 0 
          ? ((completedAnalyses / totalAnalyses) * 100).toFixed(1) 
          : 0,
        totalReports,
        accountsAnalyzed,
        averageScore: avgScore._avg.overallScore?.toFixed(1) || null,
      },
    });
  })
);

export default router;
