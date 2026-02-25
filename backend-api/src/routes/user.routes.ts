// User Routes
import { Router } from 'express';
import { z } from 'zod';
import { prisma } from '../config/database.js';
import { authenticate } from '../middleware/auth.js';
import { validateRequest } from '../middleware/validate.js';
import { asyncHandler } from '../utils/asyncHandler.js';
import { NotFoundError } from '../utils/errors.js';

const router = Router();

// Validation schemas
const updateProfileSchema = z.object({
  body: z.object({
    name: z.string().min(2).optional(),
    avatarUrl: z.string().url().nullable().optional(),
  }),
});

/**
 * @swagger
 * /api/users/profile:
 *   get:
 *     summary: Get current user profile
 *     tags: [Users]
 *     security:
 *       - bearerAuth: []
 *     responses:
 *       200:
 *         description: User profile
 */
router.get(
  '/profile',
  authenticate,
  asyncHandler(async (req, res) => {
    const user = await prisma.user.findUnique({
      where: { id: req.user!.id },
      select: {
        id: true,
        email: true,
        name: true,
        avatarUrl: true,
        emailVerified: true,
        subscriptionTier: true,
        subscriptionStatus: true,
        stripeCustomerId: true,
        trialEndsAt: true,
        createdAt: true,
        lastLoginAt: true,
        _count: {
          select: {
            analyses: true,
            instagramAccounts: true,
            reports: true,
          },
        },
      },
    });

    if (!user) {
      throw new NotFoundError('User not found');
    }

    res.json({
      success: true,
      data: user,
    });
  })
);

/**
 * @swagger
 * /api/users/profile:
 *   patch:
 *     summary: Update user profile
 *     tags: [Users]
 *     security:
 *       - bearerAuth: []
 *     requestBody:
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             properties:
 *               name:
 *                 type: string
 *               avatarUrl:
 *                 type: string
 *     responses:
 *       200:
 *         description: Profile updated
 */
router.patch(
  '/profile',
  authenticate,
  validateRequest(updateProfileSchema),
  asyncHandler(async (req, res) => {
    const { name, avatarUrl } = req.body;

    const user = await prisma.user.update({
      where: { id: req.user!.id },
      data: {
        ...(name && { name }),
        ...(avatarUrl !== undefined && { avatarUrl }),
      },
      select: {
        id: true,
        email: true,
        name: true,
        avatarUrl: true,
        emailVerified: true,
        subscriptionTier: true,
        subscriptionStatus: true,
        createdAt: true,
      },
    });

    res.json({
      success: true,
      data: user,
    });
  })
);

/**
 * @swagger
 * /api/users/accounts:
 *   get:
 *     summary: Get user's Instagram accounts
 *     tags: [Users]
 *     security:
 *       - bearerAuth: []
 *     responses:
 *       200:
 *         description: List of Instagram accounts
 */
router.get(
  '/accounts',
  authenticate,
  asyncHandler(async (req, res) => {
    const accounts = await prisma.instagramAccount.findMany({
      where: { userId: req.user!.id },
      orderBy: { lastAnalyzedAt: 'desc' },
      select: {
        id: true,
        username: true,
        followers: true,
        following: true,
        posts: true,
        bio: true,
        profilePicUrl: true,
        profilePicData: true,
        isVerified: true,
        engagementRate: true,
        botScore: true,
        analysisCount: true,
        lastAnalyzedAt: true,
        createdAt: true,
      },
    });

    // Map to prefer base64 data over CDN URL
    const accountsWithPics = accounts.map((acc) => ({
      ...acc,
      profilePicUrl: acc.profilePicData || acc.profilePicUrl,
      profilePicData: undefined, // Don't send both
    }));

    res.json({
      success: true,
      data: accountsWithPics,
    });
  })
);

/**
 * @swagger
 * /api/users/analyses:
 *   get:
 *     summary: Get user's analysis history
 *     tags: [Users]
 *     security:
 *       - bearerAuth: []
 *     parameters:
 *       - in: query
 *         name: page
 *         schema:
 *           type: integer
 *           default: 1
 *       - in: query
 *         name: limit
 *         schema:
 *           type: integer
 *           default: 10
 *       - in: query
 *         name: status
 *         schema:
 *           type: string
 *           enum: [PENDING, PROCESSING, COMPLETED, FAILED]
 *     responses:
 *       200:
 *         description: List of analyses
 */
router.get(
  '/analyses',
  authenticate,
  asyncHandler(async (req, res) => {
    const page = Math.max(1, parseInt(req.query.page as string) || 1);
    const limit = Math.min(50, Math.max(1, parseInt(req.query.limit as string) || 10));
    const status = req.query.status as string | undefined;
    const skip = (page - 1) * limit;

    const where = {
      userId: req.user!.id,
      ...(status && { status: status as any }),
    };

    const [analyses, total] = await Promise.all([
      prisma.analysis.findMany({
        where,
        skip,
        take: limit,
        orderBy: { createdAt: 'desc' },
        include: {
          account: {
            select: {
              username: true,
              profilePicUrl: true,
              profilePicData: true,
            },
          },
          reports: {
            select: {
              id: true,
              pdfUrl: true,
              reportType: true,
            },
          },
        },
      }),
      prisma.analysis.count({ where }),
    ]);

    // Map to prefer base64 data over CDN URL
    const analysesWithPics = analyses.map((a) => ({
      ...a,
      account: {
        ...a.account,
        profilePicUrl: a.account.profilePicData || a.account.profilePicUrl,
        profilePicData: undefined,
      },
    }));

    res.json({
      success: true,
      data: {
        analyses: analysesWithPics,
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

/**
 * @swagger
 * /api/users/delete:
 *   delete:
 *     summary: Delete user account
 *     tags: [Users]
 *     security:
 *       - bearerAuth: []
 *     responses:
 *       200:
 *         description: Account deleted
 */
router.delete(
  '/delete',
  authenticate,
  asyncHandler(async (req, res) => {
    // Delete user (cascades to related data)
    await prisma.user.delete({
      where: { id: req.user!.id },
    });

    res.json({
      success: true,
      message: 'Account deleted successfully',
    });
  })
);

export default router;
