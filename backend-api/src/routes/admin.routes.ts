// Admin Routes - User Management
import { Router } from 'express';
import { z } from 'zod';
import bcrypt from 'bcryptjs';
import { prisma } from '../config/database.js';
import { authenticate } from '../middleware/auth.js';
import { validateRequest } from '../middleware/validate.js';
import { asyncHandler } from '../utils/asyncHandler.js';
import { NotFoundError, ForbiddenError, BadRequestError } from '../utils/errors.js';
import { logger } from '../utils/logger.js';

const router = Router();

// Admin authentication middleware
const requireAdmin = asyncHandler(async (req, res, next) => {
  if (!req.user) {
    throw new ForbiddenError('Authentication required');
  }
  
  const user = await prisma.user.findUnique({
    where: { id: req.user.id },
    select: { isAdmin: true },
  });
  
  if (!user?.isAdmin) {
    throw new ForbiddenError('Admin access required');
  }
  
  next();
});

// Validation schemas
const createUserSchema = z.object({
  body: z.object({
    email: z.string().email('Invalid email address'),
    password: z.string().min(8, 'Password must be at least 8 characters'),
    name: z.string().min(2, 'Name must be at least 2 characters'),
    phone: z.string().optional(),
    subscriptionTier: z.enum(['FREE', 'STARTER', 'PROFESSIONAL', 'PREMIUM', 'ENTERPRISE']).optional(),
    isAdmin: z.boolean().optional(),
  }),
});

const updateUserSchema = z.object({
  body: z.object({
    email: z.string().email('Invalid email address').optional(),
    name: z.string().min(2, 'Name must be at least 2 characters').optional(),
    phone: z.string().nullable().optional(),
    subscriptionTier: z.enum(['FREE', 'STARTER', 'PROFESSIONAL', 'PREMIUM', 'ENTERPRISE']).optional(),
    subscriptionStatus: z.enum(['ACTIVE', 'CANCELLED', 'PAST_DUE', 'TRIALING', 'PAUSED']).optional(),
    isAdmin: z.boolean().optional(),
    emailVerified: z.boolean().optional(),
  }),
});

const changePasswordSchema = z.object({
  body: z.object({
    newPassword: z.string().min(8, 'Password must be at least 8 characters'),
  }),
});

const paginationSchema = z.object({
  query: z.object({
    page: z.string().optional().transform((val) => parseInt(val || '1', 10)),
    limit: z.string().optional().transform((val) => parseInt(val || '20', 10)),
    search: z.string().optional(),
    tier: z.enum(['FREE', 'STARTER', 'PROFESSIONAL', 'PREMIUM', 'ENTERPRISE']).optional(),
    status: z.enum(['ACTIVE', 'CANCELLED', 'PAST_DUE', 'TRIALING', 'PAUSED']).optional(),
  }),
});

/**
 * @swagger
 * /api/admin/users:
 *   get:
 *     summary: Get all users (Admin only)
 *     tags: [Admin]
 *     security:
 *       - bearerAuth: []
 */
router.get(
  '/users',
  authenticate,
  requireAdmin,
  validateRequest(paginationSchema),
  asyncHandler(async (req, res) => {
    const { page, limit, search, tier, status } = req.query as any;
    const skip = (page - 1) * limit;

    const where: any = {};
    
    if (search) {
      where.OR = [
        { email: { contains: search, mode: 'insensitive' } },
        { name: { contains: search, mode: 'insensitive' } },
        { phone: { contains: search, mode: 'insensitive' } },
      ];
    }
    
    if (tier) {
      where.subscriptionTier = tier;
    }
    
    if (status) {
      where.subscriptionStatus = status;
    }

    const [users, total] = await Promise.all([
      prisma.user.findMany({
        where,
        skip,
        take: limit,
        orderBy: { createdAt: 'desc' },
        select: {
          id: true,
          email: true,
          name: true,
          phone: true,
          avatarUrl: true,
          isAdmin: true,
          emailVerified: true,
          subscriptionTier: true,
          subscriptionStatus: true,
          createdAt: true,
          lastLoginAt: true,
          _count: {
            select: {
              analyses: true,
              reports: true,
            },
          },
        },
      }),
      prisma.user.count({ where }),
    ]);

    res.json({
      success: true,
      data: {
        users,
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
 * /api/admin/users/{id}:
 *   get:
 *     summary: Get user by ID (Admin only)
 *     tags: [Admin]
 *     security:
 *       - bearerAuth: []
 */
router.get(
  '/users/:id',
  authenticate,
  requireAdmin,
  asyncHandler(async (req, res) => {
    const { id } = req.params;

    const user = await prisma.user.findUnique({
      where: { id },
      select: {
        id: true,
        email: true,
        name: true,
        phone: true,
        avatarUrl: true,
        isAdmin: true,
        emailVerified: true,
        subscriptionTier: true,
        subscriptionStatus: true,
        stripeCustomerId: true,
        stripeSubscriptionId: true,
        trialEndsAt: true,
        createdAt: true,
        updatedAt: true,
        lastLoginAt: true,
        _count: {
          select: {
            analyses: true,
            reports: true,
            instagramAccounts: true,
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
 * /api/admin/users:
 *   post:
 *     summary: Create new user (Admin only)
 *     tags: [Admin]
 *     security:
 *       - bearerAuth: []
 */
router.post(
  '/users',
  authenticate,
  requireAdmin,
  validateRequest(createUserSchema),
  asyncHandler(async (req, res) => {
    const { email, password, name, phone, subscriptionTier, isAdmin } = req.body;

    // Check if email already exists
    const existingUser = await prisma.user.findUnique({
      where: { email },
    });

    if (existingUser) {
      throw new BadRequestError('Email already registered');
    }

    // Hash password
    const passwordHash = await bcrypt.hash(password, 12);

    const user = await prisma.user.create({
      data: {
        email,
        passwordHash,
        name,
        phone,
        subscriptionTier: subscriptionTier || 'STARTER',
        subscriptionStatus: 'ACTIVE',
        isAdmin: isAdmin || false,
        emailVerified: true, // Admin-created users are auto-verified
      },
      select: {
        id: true,
        email: true,
        name: true,
        phone: true,
        isAdmin: true,
        subscriptionTier: true,
        subscriptionStatus: true,
        createdAt: true,
      },
    });

    logger.info(`Admin ${req.user!.email} created user: ${email}`);

    res.status(201).json({
      success: true,
      data: user,
      message: 'User created successfully',
    });
  })
);

/**
 * @swagger
 * /api/admin/users/{id}:
 *   patch:
 *     summary: Update user (Admin only)
 *     tags: [Admin]
 *     security:
 *       - bearerAuth: []
 */
router.patch(
  '/users/:id',
  authenticate,
  requireAdmin,
  validateRequest(updateUserSchema),
  asyncHandler(async (req, res) => {
    const { id } = req.params;
    const { email, name, phone, subscriptionTier, subscriptionStatus, isAdmin, emailVerified } = req.body;

    // Check if user exists
    const existingUser = await prisma.user.findUnique({
      where: { id },
    });

    if (!existingUser) {
      throw new NotFoundError('User not found');
    }

    // If email is being changed, check for duplicates
    if (email && email !== existingUser.email) {
      const emailExists = await prisma.user.findUnique({
        where: { email },
      });
      if (emailExists) {
        throw new BadRequestError('Email already in use');
      }
    }

    const user = await prisma.user.update({
      where: { id },
      data: {
        ...(email && { email }),
        ...(name && { name }),
        ...(phone !== undefined && { phone }),
        ...(subscriptionTier && { subscriptionTier }),
        ...(subscriptionStatus && { subscriptionStatus }),
        ...(isAdmin !== undefined && { isAdmin }),
        ...(emailVerified !== undefined && { emailVerified }),
      },
      select: {
        id: true,
        email: true,
        name: true,
        phone: true,
        isAdmin: true,
        emailVerified: true,
        subscriptionTier: true,
        subscriptionStatus: true,
        updatedAt: true,
      },
    });

    logger.info(`Admin ${req.user!.email} updated user: ${id}`);

    res.json({
      success: true,
      data: user,
      message: 'User updated successfully',
    });
  })
);

/**
 * @swagger
 * /api/admin/users/{id}/password:
 *   patch:
 *     summary: Change user password (Admin only)
 *     tags: [Admin]
 *     security:
 *       - bearerAuth: []
 */
router.patch(
  '/users/:id/password',
  authenticate,
  requireAdmin,
  validateRequest(changePasswordSchema),
  asyncHandler(async (req, res) => {
    const { id } = req.params;
    const { newPassword } = req.body;

    // Check if user exists
    const existingUser = await prisma.user.findUnique({
      where: { id },
    });

    if (!existingUser) {
      throw new NotFoundError('User not found');
    }

    // Hash new password
    const passwordHash = await bcrypt.hash(newPassword, 12);

    await prisma.user.update({
      where: { id },
      data: { passwordHash },
    });

    // Revoke all refresh tokens for security
    await prisma.refreshToken.updateMany({
      where: { userId: id, revokedAt: null },
      data: { revokedAt: new Date() },
    });

    logger.info(`Admin ${req.user!.email} changed password for user: ${id}`);

    res.json({
      success: true,
      message: 'Password changed successfully. User will need to log in again.',
    });
  })
);

/**
 * @swagger
 * /api/admin/users/{id}:
 *   delete:
 *     summary: Delete user (Admin only)
 *     tags: [Admin]
 *     security:
 *       - bearerAuth: []
 */
router.delete(
  '/users/:id',
  authenticate,
  requireAdmin,
  asyncHandler(async (req, res) => {
    const { id } = req.params;

    // Prevent self-deletion
    if (id === req.user!.id) {
      throw new BadRequestError('Cannot delete your own account');
    }

    // Check if user exists
    const existingUser = await prisma.user.findUnique({
      where: { id },
    });

    if (!existingUser) {
      throw new NotFoundError('User not found');
    }

    await prisma.user.delete({
      where: { id },
    });

    logger.info(`Admin ${req.user!.email} deleted user: ${id} (${existingUser.email})`);

    res.json({
      success: true,
      message: 'User deleted successfully',
    });
  })
);

/**
 * @swagger
 * /api/admin/stats:
 *   get:
 *     summary: Get admin dashboard stats (Admin only)
 *     tags: [Admin]
 *     security:
 *       - bearerAuth: []
 */
router.get(
  '/stats',
  authenticate,
  requireAdmin,
  asyncHandler(async (req, res) => {
    const [
      totalUsers,
      activeUsers,
      totalAnalyses,
      totalReports,
      usersByTier,
      recentUsers,
      recentAnalyses,
    ] = await Promise.all([
      prisma.user.count(),
      prisma.user.count({
        where: { subscriptionStatus: 'ACTIVE' },
      }),
      prisma.analysis.count(),
      prisma.report.count(),
      prisma.user.groupBy({
        by: ['subscriptionTier'],
        _count: true,
      }),
      prisma.user.findMany({
        take: 5,
        orderBy: { createdAt: 'desc' },
        select: {
          id: true,
          email: true,
          name: true,
          subscriptionTier: true,
          createdAt: true,
        },
      }),
      prisma.analysis.findMany({
        take: 5,
        orderBy: { createdAt: 'desc' },
        select: {
          id: true,
          status: true,
          createdAt: true,
          account: {
            select: {
              username: true,
            },
          },
          user: {
            select: {
              email: true,
            },
          },
        },
      }),
    ]);

    res.json({
      success: true,
      data: {
        totalUsers,
        activeUsers,
        totalAnalyses,
        totalReports,
        usersByTier: usersByTier.reduce((acc, item) => {
          acc[item.subscriptionTier] = item._count;
          return acc;
        }, {} as Record<string, number>),
        recentUsers,
        recentAnalyses,
      },
    });
  })
);

export default router;
