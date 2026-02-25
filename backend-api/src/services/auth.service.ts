// Authentication Service
import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';
import crypto from 'crypto';
import { v4 as uuidv4 } from 'uuid';
import { prisma } from '../config/database.js';
import { config } from '../config/index.js';
import { redis } from '../config/redis.js';
import {
  BadRequestError,
  UnauthorizedError,
  ConflictError,
  NotFoundError,
} from '../utils/errors.js';
import { emailService } from './email.service.js';
import { logger } from '../utils/logger.js';

interface RegisterInput {
  email: string;
  password: string;
  name: string;
}

interface LoginInput {
  email: string;
  password: string;
  ipAddress?: string;
  userAgent?: string;
}

interface AuthTokens {
  accessToken: string;
  refreshToken: string;
  expiresIn: number;
}

interface UserResponse {
  id: string;
  email: string;
  name: string;
  avatarUrl: string | null;
  emailVerified: boolean;
  subscriptionTier: string;
  subscriptionStatus: string;
  createdAt: Date;
}

class AuthService {
  private readonly SALT_ROUNDS = 12;
  private readonly ACCESS_TOKEN_EXPIRY = '15m';
  private readonly REFRESH_TOKEN_EXPIRY = '7d';
  private readonly REFRESH_TOKEN_EXPIRY_SECONDS = 7 * 24 * 60 * 60;
  private readonly PASSWORD_RESET_EXPIRY = 60 * 60 * 1000; // 1 hour

  // Register new user
  async register(input: RegisterInput): Promise<{ user: UserResponse; tokens: AuthTokens }> {
    const { email, password, name } = input;

    // Check if user exists
    const existingUser = await prisma.user.findUnique({
      where: { email: email.toLowerCase() },
    });

    if (existingUser) {
      throw new ConflictError('Email already registered');
    }

    // Hash password
    const passwordHash = await bcrypt.hash(password, this.SALT_ROUNDS);

    // Generate email verification token
    const emailVerificationToken = this.generateToken();

    // Create user
    const user = await prisma.user.create({
      data: {
        email: email.toLowerCase(),
        passwordHash,
        name,
        emailVerificationToken,
        subscriptionTier: 'STARTER',
        subscriptionStatus: 'TRIALING',
        trialEndsAt: new Date(Date.now() + 14 * 24 * 60 * 60 * 1000), // 14 days trial
      },
    });

    // Generate tokens
    const tokens = await this.generateAuthTokens(user.id, user.email);

    // Send verification email
    try {
      await emailService.sendVerificationEmail(user.email, user.name, emailVerificationToken);
    } catch (error) {
      logger.error('Failed to send verification email:', error);
      // Don't fail registration if email fails
    }

    return {
      user: this.formatUserResponse(user),
      tokens,
    };
  }

  // Login user
  async login(input: LoginInput): Promise<{ user: UserResponse; tokens: AuthTokens }> {
    const { email, password, ipAddress, userAgent } = input;

    // Find user
    const user = await prisma.user.findUnique({
      where: { email: email.toLowerCase() },
    });

    if (!user) {
      throw new UnauthorizedError('Invalid email or password');
    }

    // Verify password
    const isValidPassword = await bcrypt.compare(password, user.passwordHash);

    if (!isValidPassword) {
      throw new UnauthorizedError('Invalid email or password');
    }

    // Update last login
    await prisma.user.update({
      where: { id: user.id },
      data: { lastLoginAt: new Date() },
    });

    // Generate tokens
    const tokens = await this.generateAuthTokens(user.id, user.email, ipAddress, userAgent);

    return {
      user: this.formatUserResponse(user),
      tokens,
    };
  }

  // Logout user (revoke refresh token)
  async logout(refreshToken: string): Promise<void> {
    // Find and revoke refresh token
    const token = await prisma.refreshToken.findUnique({
      where: { token: refreshToken },
    });

    if (token) {
      await prisma.refreshToken.update({
        where: { id: token.id },
        data: { revokedAt: new Date() },
      });
    }

    // Add token to blacklist
    await redis.setex(`blacklist:${refreshToken}`, this.REFRESH_TOKEN_EXPIRY_SECONDS, '1');
  }

  // Refresh access token
  async refreshAccessToken(refreshToken: string): Promise<AuthTokens> {
    // Check blacklist
    const isBlacklisted = await redis.get(`blacklist:${refreshToken}`);
    if (isBlacklisted) {
      throw new UnauthorizedError('Token has been revoked');
    }

    // Verify refresh token
    let decoded: { userId: string; email: string; type: string };
    try {
      decoded = jwt.verify(refreshToken, config.jwt.secret) as typeof decoded;
    } catch {
      throw new UnauthorizedError('Invalid refresh token');
    }

    if (decoded.type !== 'refresh') {
      throw new UnauthorizedError('Invalid token type');
    }

    // Find token in database
    const storedToken = await prisma.refreshToken.findUnique({
      where: { token: refreshToken },
      include: { user: true },
    });

    if (!storedToken || storedToken.revokedAt) {
      throw new UnauthorizedError('Token has been revoked');
    }

    if (storedToken.expiresAt < new Date()) {
      throw new UnauthorizedError('Token has expired');
    }

    // Revoke old refresh token
    await prisma.refreshToken.update({
      where: { id: storedToken.id },
      data: { revokedAt: new Date() },
    });

    // Generate new tokens
    return this.generateAuthTokens(storedToken.userId, storedToken.user.email);
  }

  // Request password reset
  async forgotPassword(email: string): Promise<void> {
    const user = await prisma.user.findUnique({
      where: { email: email.toLowerCase() },
    });

    // Always return success to prevent email enumeration
    if (!user) {
      return;
    }

    // Generate reset token
    const resetToken = this.generateToken();
    const resetExpires = new Date(Date.now() + this.PASSWORD_RESET_EXPIRY);

    // Save reset token
    await prisma.user.update({
      where: { id: user.id },
      data: {
        passwordResetToken: resetToken,
        passwordResetExpires: resetExpires,
      },
    });

    // Send reset email
    try {
      await emailService.sendPasswordResetEmail(user.email, user.name, resetToken);
    } catch (error) {
      logger.error('Failed to send password reset email:', error);
      throw new Error('Failed to send password reset email');
    }
  }

  // Reset password
  async resetPassword(token: string, newPassword: string): Promise<void> {
    const user = await prisma.user.findFirst({
      where: {
        passwordResetToken: token,
        passwordResetExpires: { gt: new Date() },
      },
    });

    if (!user) {
      throw new BadRequestError('Invalid or expired reset token');
    }

    // Hash new password
    const passwordHash = await bcrypt.hash(newPassword, this.SALT_ROUNDS);

    // Update password and clear reset token
    await prisma.user.update({
      where: { id: user.id },
      data: {
        passwordHash,
        passwordResetToken: null,
        passwordResetExpires: null,
      },
    });

    // Revoke all refresh tokens
    await prisma.refreshToken.updateMany({
      where: { userId: user.id },
      data: { revokedAt: new Date() },
    });
  }

  // Verify email
  async verifyEmail(token: string): Promise<void> {
    const user = await prisma.user.findFirst({
      where: { emailVerificationToken: token },
    });

    if (!user) {
      throw new BadRequestError('Invalid verification token');
    }

    await prisma.user.update({
      where: { id: user.id },
      data: {
        emailVerified: true,
        emailVerificationToken: null,
      },
    });
  }

  // Resend verification email
  async resendVerificationEmail(userId: string): Promise<void> {
    const user = await prisma.user.findUnique({
      where: { id: userId },
    });

    if (!user) {
      throw new NotFoundError('User not found');
    }

    if (user.emailVerified) {
      throw new BadRequestError('Email already verified');
    }

    // Generate new token
    const emailVerificationToken = this.generateToken();

    await prisma.user.update({
      where: { id: user.id },
      data: { emailVerificationToken },
    });

    await emailService.sendVerificationEmail(user.email, user.name, emailVerificationToken);
  }

  // Change password
  async changePassword(
    userId: string,
    currentPassword: string,
    newPassword: string
  ): Promise<void> {
    const user = await prisma.user.findUnique({
      where: { id: userId },
    });

    if (!user) {
      throw new NotFoundError('User not found');
    }

    // Verify current password
    const isValidPassword = await bcrypt.compare(currentPassword, user.passwordHash);
    if (!isValidPassword) {
      throw new BadRequestError('Current password is incorrect');
    }

    // Hash new password
    const passwordHash = await bcrypt.hash(newPassword, this.SALT_ROUNDS);

    await prisma.user.update({
      where: { id: userId },
      data: { passwordHash },
    });
  }

  // Generate auth tokens
  private async generateAuthTokens(
    userId: string,
    email: string,
    ipAddress?: string,
    userAgent?: string
  ): Promise<AuthTokens> {
    // Generate access token
    const accessToken = jwt.sign(
      { userId, email, type: 'access' },
      config.jwt.secret,
      { expiresIn: this.ACCESS_TOKEN_EXPIRY }
    );

    // Generate refresh token
    const refreshToken = jwt.sign(
      { userId, email, type: 'refresh' },
      config.jwt.secret,
      { expiresIn: this.REFRESH_TOKEN_EXPIRY }
    );

    // Store refresh token in database
    await prisma.refreshToken.create({
      data: {
        token: refreshToken,
        userId,
        expiresAt: new Date(Date.now() + this.REFRESH_TOKEN_EXPIRY_SECONDS * 1000),
        ipAddress,
        userAgent,
      },
    });

    return {
      accessToken,
      refreshToken,
      expiresIn: 900, // 15 minutes in seconds
    };
  }

  // Generate random token
  private generateToken(): string {
    return crypto.randomBytes(32).toString('hex');
  }

  // Format user response
  private formatUserResponse(user: any): UserResponse {
    return {
      id: user.id,
      email: user.email,
      name: user.name,
      avatarUrl: user.avatarUrl,
      emailVerified: user.emailVerified,
      subscriptionTier: user.subscriptionTier,
      subscriptionStatus: user.subscriptionStatus,
      createdAt: user.createdAt,
    };
  }
}

export const authService = new AuthService();
