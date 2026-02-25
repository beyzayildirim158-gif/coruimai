// Rate Limiting Middleware
import { Request, Response, NextFunction } from 'express';
import rateLimit from 'express-rate-limit';
import { redis, cache } from '../config/redis.js';
import { tierLimits, SubscriptionTier } from '../config/index.js';
import { RateLimitError, ForbiddenError } from '../utils/errors.js';
import { prisma } from '../config/database.js';
import { logger } from '../utils/logger.js';

// Basic rate limiter for unauthenticated requests
export const basicRateLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100,
  message: {
    success: false,
    error: {
      code: 'RATE_LIMIT_EXCEEDED',
      message: 'Too many requests, please try again later',
    },
  },
  standardHeaders: true,
  legacyHeaders: false,
});

// Login rate limiter (50 attempts per 15 minutes for development)
export const loginRateLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 50,
  message: {
    success: false,
    error: {
      code: 'TOO_MANY_LOGIN_ATTEMPTS',
      message: 'Too many login attempts, please try again in 15 minutes',
    },
  },
  standardHeaders: true,
  legacyHeaders: false,
  keyGenerator: (req) => req.body?.email || req.ip || 'unknown',
});

// Tier-based rate limiter for API requests
export const tierRateLimiter = async (
  req: Request,
  res: Response,
  next: NextFunction
): Promise<void> => {
  try {
    if (!req.user) {
      return next();
    }

    const tier = req.user.subscriptionTier as SubscriptionTier;
    const limits = tierLimits[tier];
    const key = `ratelimit:${req.user.id}:${getCurrentHour()}`;

    // Get current request count
    const currentCount = await redis.incr(key);
    
    // Set expiry on first request
    if (currentCount === 1) {
      await redis.expire(key, 3600); // 1 hour
    }

    // Check if limit exceeded
    if (currentCount > limits.requestsPerHour) {
      const ttl = await redis.ttl(key);
      res.setHeader('X-RateLimit-Limit', limits.requestsPerHour.toString());
      res.setHeader('X-RateLimit-Remaining', '0');
      res.setHeader('X-RateLimit-Reset', (Math.floor(Date.now() / 1000) + ttl).toString());
      res.setHeader('Retry-After', ttl.toString());
      
      throw new RateLimitError(
        `Rate limit exceeded. Limit: ${limits.requestsPerHour} requests per hour`,
        ttl
      );
    }

    // Set rate limit headers
    res.setHeader('X-RateLimit-Limit', limits.requestsPerHour.toString());
    res.setHeader('X-RateLimit-Remaining', (limits.requestsPerHour - currentCount).toString());
    
    const ttl = await redis.ttl(key);
    res.setHeader('X-RateLimit-Reset', (Math.floor(Date.now() / 1000) + ttl).toString());

    next();
  } catch (error) {
    if (error instanceof RateLimitError) {
      next(error);
    } else {
      logger.error('Rate limiter error:', error);
      next(); // Continue on error to not block requests
    }
  }
};

// Analysis usage limiter (monthly limit)
export const analysisLimiter = async (
  req: Request,
  _res: Response,
  next: NextFunction
): Promise<void> => {
  try {
    if (!req.user) {
      return next();
    }

    const tier = req.user.subscriptionTier as SubscriptionTier;
    const limits = tierLimits[tier];
    
    // Enterprise has unlimited analyses
    if (limits.analysesPerMonth === -1) {
      return next();
    }

    const monthYear = getCurrentMonthYear();
    
    // Get or create usage record
    const usage = await prisma.apiUsage.upsert({
      where: {
        userId_monthYear: {
          userId: req.user.id,
          monthYear,
        },
      },
      create: {
        userId: req.user.id,
        endpoint: req.path,
        method: req.method,
        date: new Date(),
        analysesUsed: 0,
        monthYear,
      },
      update: {},
    });

    // Check if limit exceeded
    if (usage.analysesUsed >= limits.analysesPerMonth) {
      throw new ForbiddenError(
        `Monthly analysis limit reached (${limits.analysesPerMonth}). Upgrade your plan for more analyses.`
      );
    }

    next();
  } catch (error) {
    if (error instanceof ForbiddenError) {
      next(error);
    } else {
      logger.error('Analysis limiter error:', error);
      next(); // Continue on error
    }
  }
};

// Increment analysis usage after successful analysis start
export const incrementAnalysisUsage = async (userId: string): Promise<void> => {
  const monthYear = getCurrentMonthYear();
  
  await prisma.apiUsage.upsert({
    where: {
      userId_monthYear: {
        userId,
        monthYear,
      },
    },
    create: {
      userId,
      endpoint: '/api/analyze/start',
      method: 'POST',
      date: new Date(),
      analysesUsed: 1,
      monthYear,
    },
    update: {
      analysesUsed: {
        increment: 1,
      },
    },
  });
};

// Get current month analysis usage
export const getAnalysisUsage = async (userId: string): Promise<{
  used: number;
  limit: number;
  remaining: number;
}> => {
  const user = await prisma.user.findUnique({
    where: { id: userId },
    select: { subscriptionTier: true },
  });

  if (!user) {
    throw new Error('User not found');
  }

  const tier = user.subscriptionTier as SubscriptionTier;
  const limits = tierLimits[tier];
  const monthYear = getCurrentMonthYear();

  const usage = await prisma.apiUsage.findUnique({
    where: {
      userId_monthYear: {
        userId,
        monthYear,
      },
    },
  });

  const used = usage?.analysesUsed || 0;
  const limit = limits.analysesPerMonth;
  
  return {
    used,
    limit,
    remaining: limit === -1 ? -1 : Math.max(0, limit - used),
  };
};

// Helper functions
function getCurrentHour(): string {
  const now = new Date();
  return `${now.getUTCFullYear()}-${now.getUTCMonth()}-${now.getUTCDate()}-${now.getUTCHours()}`;
}

function getCurrentMonthYear(): string {
  const now = new Date();
  return `${now.getUTCFullYear()}-${String(now.getUTCMonth() + 1).padStart(2, '0')}`;
}
