// Authentication Middleware
import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';
import { config } from '../config/index.js';
import { prisma } from '../config/database.js';
import { UnauthorizedError, ForbiddenError } from '../utils/errors.js';
import { SubscriptionTier } from '@prisma/client';

// Extend Express Request type
declare global {
  namespace Express {
    interface Request {
      user?: {
        id: string;
        email: string;
        name: string;
        subscriptionTier: SubscriptionTier;
        subscriptionStatus: string;
      };
    }
  }
}

interface JWTPayload {
  userId: string;
  email: string;
  type: 'access' | 'refresh';
  iat: number;
  exp: number;
}

// Verify JWT and attach user to request
export const authenticate = async (
  req: Request,
  _res: Response,
  next: NextFunction
): Promise<void> => {
  try {
    const authHeader = req.headers.authorization;
    
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      throw new UnauthorizedError('No token provided');
    }

    const token = authHeader.split(' ')[1];
    
    if (!token) {
      throw new UnauthorizedError('Invalid token format');
    }

    // Verify token
    const decoded = jwt.verify(token, config.jwt.secret) as JWTPayload;
    
    if (decoded.type !== 'access') {
      throw new UnauthorizedError('Invalid token type');
    }

    // Fetch user from database
    const user = await prisma.user.findUnique({
      where: { id: decoded.userId },
      select: {
        id: true,
        email: true,
        name: true,
        subscriptionTier: true,
        subscriptionStatus: true,
        emailVerified: true,
      },
    });

    if (!user) {
      throw new UnauthorizedError('User not found');
    }

    // Check if subscription is active
    if (user.subscriptionStatus === 'CANCELLED' || user.subscriptionStatus === 'PAST_DUE') {
      throw new ForbiddenError('Subscription is not active');
    }

    // Attach user to request
    req.user = {
      id: user.id,
      email: user.email,
      name: user.name,
      subscriptionTier: user.subscriptionTier,
      subscriptionStatus: user.subscriptionStatus,
    };

    next();
  } catch (error) {
    if (error instanceof UnauthorizedError || error instanceof ForbiddenError) {
      next(error);
    } else if (error instanceof jwt.JsonWebTokenError) {
      // Log JWT errors for debugging (but don't expose details to client)
      const errorDetails = {
        name: error.name,
        message: error.message,
        tokenPreview: req.headers.authorization?.substring(0, 20) + '...',
      };
      console.error('[Auth] JWT Validation Error:', errorDetails);
      next(new UnauthorizedError('Invalid token'));
    } else if (error instanceof jwt.TokenExpiredError) {
      console.error('[Auth] Token expired at:', error.expiredAt);
      next(new UnauthorizedError('Token expired. Please login again.'));
    } else {
      console.error('[Auth] Unexpected auth error:', error);
      next(error);
    }
  }
};

// Optional authentication - doesn't fail if no token
export const optionalAuth = async (
  req: Request,
  _res: Response,
  next: NextFunction
): Promise<void> => {
  try {
    const authHeader = req.headers.authorization;
    
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return next();
    }

    const token = authHeader.split(' ')[1];
    
    if (!token) {
      return next();
    }

    const decoded = jwt.verify(token, config.jwt.secret) as JWTPayload;
    
    if (decoded.type !== 'access') {
      return next();
    }

    const user = await prisma.user.findUnique({
      where: { id: decoded.userId },
      select: {
        id: true,
        email: true,
        name: true,
        subscriptionTier: true,
        subscriptionStatus: true,
      },
    });

    if (user) {
      req.user = {
        id: user.id,
        email: user.email,
        name: user.name,
        subscriptionTier: user.subscriptionTier,
        subscriptionStatus: user.subscriptionStatus,
      };
    }

    next();
  } catch {
    // Silently continue without authentication
    next();
  }
};

// Require email verification
export const requireEmailVerified = async (
  req: Request,
  _res: Response,
  next: NextFunction
): Promise<void> => {
  try {
    if (!req.user) {
      throw new UnauthorizedError('Authentication required');
    }

    const user = await prisma.user.findUnique({
      where: { id: req.user.id },
      select: { emailVerified: true },
    });

    if (!user?.emailVerified) {
      throw new ForbiddenError('Email verification required');
    }

    next();
  } catch (error) {
    next(error);
  }
};

// Require specific subscription tier
export const requireTier = (allowedTiers: SubscriptionTier[]) => {
  return (req: Request, _res: Response, next: NextFunction): void => {
    if (!req.user) {
      return next(new UnauthorizedError('Authentication required'));
    }

    if (!allowedTiers.includes(req.user.subscriptionTier)) {
      return next(new ForbiddenError(
        `This feature requires ${allowedTiers.join(' or ')} subscription`
      ));
    }

    next();
  };
};

// Require minimum subscription tier
export const requireMinTier = (minTier: SubscriptionTier) => {
  const tierOrder: SubscriptionTier[] = ['STARTER', 'PROFESSIONAL', 'PREMIUM', 'ENTERPRISE'];
  const minIndex = tierOrder.indexOf(minTier);
  
  return (req: Request, _res: Response, next: NextFunction): void => {
    if (!req.user) {
      return next(new UnauthorizedError('Authentication required'));
    }

    const userIndex = tierOrder.indexOf(req.user.subscriptionTier);
    
    if (userIndex < minIndex) {
      return next(new ForbiddenError(
        `This feature requires ${minTier} subscription or higher`
      ));
    }

    next();
  };
};
