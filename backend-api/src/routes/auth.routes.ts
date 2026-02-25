// Authentication Routes
import { Router } from 'express';
import { z } from 'zod';
import { authService } from '../services/auth.service.js';
import { authenticate } from '../middleware/auth.js';
import { loginRateLimiter } from '../middleware/rateLimiter.js';
import { validateRequest } from '../middleware/validate.js';
import { asyncHandler } from '../utils/asyncHandler.js';

const router = Router();

// Validation schemas
const registerSchema = z.object({
  body: z.object({
    email: z.string().email('Invalid email address'),
    password: z
      .string()
      .min(8, 'Password must be at least 8 characters')
      .regex(
        /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/,
        'Password must contain at least one uppercase letter, one lowercase letter, and one number'
      ),
    name: z.string().min(2, 'Name must be at least 2 characters'),
  }),
});

const loginSchema = z.object({
  body: z.object({
    email: z.string().email('Invalid email address'),
    password: z.string().min(1, 'Password is required'),
  }),
});

const forgotPasswordSchema = z.object({
  body: z.object({
    email: z.string().email('Invalid email address'),
  }),
});

const resetPasswordSchema = z.object({
  body: z.object({
    token: z.string().min(1, 'Token is required'),
    password: z
      .string()
      .min(8, 'Password must be at least 8 characters')
      .regex(
        /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/,
        'Password must contain at least one uppercase letter, one lowercase letter, and one number'
      ),
  }),
});

const changePasswordSchema = z.object({
  body: z.object({
    currentPassword: z.string().min(1, 'Current password is required'),
    newPassword: z
      .string()
      .min(8, 'Password must be at least 8 characters')
      .regex(
        /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/,
        'Password must contain at least one uppercase letter, one lowercase letter, and one number'
      ),
  }),
});

/**
 * @swagger
 * /api/auth/register:
 *   post:
 *     summary: Register a new user
 *     tags: [Authentication]
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required: [email, password, name]
 *             properties:
 *               email:
 *                 type: string
 *                 format: email
 *                 example: user@example.com
 *               password:
 *                 type: string
 *                 minLength: 8
 *                 example: Password123
 *               name:
 *                 type: string
 *                 example: John Doe
 *     responses:
 *       201:
 *         description: User registered successfully
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 success:
 *                   type: boolean
 *                 data:
 *                   type: object
 *                   properties:
 *                     user:
 *                       $ref: '#/components/schemas/User'
 *                     tokens:
 *                       $ref: '#/components/schemas/AuthTokens'
 *       400:
 *         $ref: '#/components/responses/ValidationError'
 *       409:
 *         description: Email already registered
 */
router.post(
  '/register',
  validateRequest(registerSchema),
  asyncHandler(async (req, res) => {
    const { email, password, name } = req.body;
    const result = await authService.register({ email, password, name });

    res.status(201).json({
      success: true,
      data: result,
    });
  })
);

/**
 * @swagger
 * /api/auth/login:
 *   post:
 *     summary: Login user
 *     tags: [Authentication]
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required: [email, password]
 *             properties:
 *               email:
 *                 type: string
 *                 format: email
 *               password:
 *                 type: string
 *     responses:
 *       200:
 *         description: Login successful
 *       401:
 *         description: Invalid credentials
 *       429:
 *         description: Too many login attempts
 */
router.post(
  '/login',
  loginRateLimiter,
  validateRequest(loginSchema),
  asyncHandler(async (req, res) => {
    const { email, password } = req.body;
    const result = await authService.login({
      email,
      password,
      ipAddress: req.ip,
      userAgent: req.headers['user-agent'],
    });

    // Set refresh token as HttpOnly cookie
    res.cookie('refreshToken', result.tokens.refreshToken, {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      sameSite: process.env.NODE_ENV === 'production' ? 'strict' : 'lax',
      maxAge: 7 * 24 * 60 * 60 * 1000, // 7 days
      path: '/',
    });

    res.json({
      success: true,
      data: result,
    });
  })
);

/**
 * @swagger
 * /api/auth/logout:
 *   post:
 *     summary: Logout user
 *     tags: [Authentication]
 *     security:
 *       - bearerAuth: []
 *     responses:
 *       200:
 *         description: Logout successful
 */
router.post(
  '/logout',
  asyncHandler(async (req, res) => {
    const refreshToken = req.cookies?.refreshToken || req.body.refreshToken;

    if (refreshToken) {
      await authService.logout(refreshToken);
    }

    res.clearCookie('refreshToken');

    res.json({
      success: true,
      message: 'Logged out successfully',
    });
  })
);

/**
 * @swagger
 * /api/auth/refresh:
 *   post:
 *     summary: Refresh access token
 *     tags: [Authentication]
 *     requestBody:
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             properties:
 *               refreshToken:
 *                 type: string
 *     responses:
 *       200:
 *         description: Tokens refreshed successfully
 *       401:
 *         description: Invalid refresh token
 */
router.post(
  '/refresh',
  asyncHandler(async (req, res) => {
    const refreshToken = req.cookies?.refreshToken || req.body.refreshToken;

    if (!refreshToken) {
      return res.status(401).json({
        success: false,
        error: {
          code: 'NO_REFRESH_TOKEN',
          message: 'Refresh token is required',
        },
      });
    }

    const tokens = await authService.refreshAccessToken(refreshToken);

    // Update refresh token cookie
    res.cookie('refreshToken', tokens.refreshToken, {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'lax',
      maxAge: 7 * 24 * 60 * 60 * 1000,
    });

    res.json({
      success: true,
      data: tokens,
    });
  })
);

/**
 * @swagger
 * /api/auth/forgot-password:
 *   post:
 *     summary: Request password reset
 *     tags: [Authentication]
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required: [email]
 *             properties:
 *               email:
 *                 type: string
 *                 format: email
 *     responses:
 *       200:
 *         description: Reset email sent (if account exists)
 */
router.post(
  '/forgot-password',
  validateRequest(forgotPasswordSchema),
  asyncHandler(async (req, res) => {
    const { email } = req.body;
    await authService.forgotPassword(email);

    res.json({
      success: true,
      message: 'If an account exists with this email, a password reset link has been sent',
    });
  })
);

/**
 * @swagger
 * /api/auth/reset-password:
 *   post:
 *     summary: Reset password with token
 *     tags: [Authentication]
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required: [token, password]
 *             properties:
 *               token:
 *                 type: string
 *               password:
 *                 type: string
 *                 minLength: 8
 *     responses:
 *       200:
 *         description: Password reset successful
 *       400:
 *         description: Invalid or expired token
 */
router.post(
  '/reset-password',
  validateRequest(resetPasswordSchema),
  asyncHandler(async (req, res) => {
    const { token, password } = req.body;
    await authService.resetPassword(token, password);

    res.json({
      success: true,
      message: 'Password reset successful',
    });
  })
);

/**
 * @swagger
 * /api/auth/verify-email/{token}:
 *   get:
 *     summary: Verify email address
 *     tags: [Authentication]
 *     parameters:
 *       - in: path
 *         name: token
 *         required: true
 *         schema:
 *           type: string
 *     responses:
 *       200:
 *         description: Email verified successfully
 *       400:
 *         description: Invalid verification token
 */
router.get(
  '/verify-email/:token',
  asyncHandler(async (req, res) => {
    const { token } = req.params;
    await authService.verifyEmail(token);

    res.json({
      success: true,
      message: 'Email verified successfully',
    });
  })
);

/**
 * @swagger
 * /api/auth/resend-verification:
 *   post:
 *     summary: Resend verification email
 *     tags: [Authentication]
 *     security:
 *       - bearerAuth: []
 *     responses:
 *       200:
 *         description: Verification email sent
 */
router.post(
  '/resend-verification',
  authenticate,
  asyncHandler(async (req, res) => {
    await authService.resendVerificationEmail(req.user!.id);

    res.json({
      success: true,
      message: 'Verification email sent',
    });
  })
);

/**
 * @swagger
 * /api/auth/change-password:
 *   post:
 *     summary: Change password (authenticated)
 *     tags: [Authentication]
 *     security:
 *       - bearerAuth: []
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required: [currentPassword, newPassword]
 *             properties:
 *               currentPassword:
 *                 type: string
 *               newPassword:
 *                 type: string
 *                 minLength: 8
 *     responses:
 *       200:
 *         description: Password changed successfully
 */
router.post(
  '/change-password',
  authenticate,
  validateRequest(changePasswordSchema),
  asyncHandler(async (req, res) => {
    const { currentPassword, newPassword } = req.body;
    await authService.changePassword(req.user!.id, currentPassword, newPassword);

    res.json({
      success: true,
      message: 'Password changed successfully',
    });
  })
);

/**
 * @swagger
 * /api/auth/me:
 *   get:
 *     summary: Get current user
 *     tags: [Authentication]
 *     security:
 *       - bearerAuth: []
 *     responses:
 *       200:
 *         description: Current user data
 */
router.get(
  '/me',
  authenticate,
  asyncHandler(async (req, res) => {
    res.json({
      success: true,
      data: req.user,
    });
  })
);

export default router;
