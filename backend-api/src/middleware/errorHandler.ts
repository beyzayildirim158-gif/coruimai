// Error Handler Middleware
import { Request, Response, NextFunction } from 'express';
import { AppError, RateLimitError } from '../utils/errors.js';
import { logger } from '../utils/logger.js';
import { ZodError } from 'zod';
import { Prisma } from '@prisma/client';

interface ErrorResponse {
  success: false;
  error: {
    code: string;
    message: string;
    details?: Record<string, unknown>;
    stack?: string;
  };
}

export const errorHandler = (
  err: Error,
  req: Request,
  res: Response,
  _next: NextFunction
): void => {
  logger.error(`Error: ${err.message}`, {
    error: err,
    path: req.path,
    method: req.method,
    ip: req.ip,
    userId: (req as any).user?.id,
  });

  const response: ErrorResponse = {
    success: false,
    error: {
      code: 'INTERNAL_ERROR',
      message: 'An unexpected error occurred',
    },
  };

  let statusCode = 500;

  // Handle custom AppError
  if (err instanceof AppError) {
    statusCode = err.statusCode;
    response.error.code = err.code;
    response.error.message = err.message;
    if (err.details) {
      response.error.details = err.details;
    }

    // Add retry-after header for rate limit errors
    if (err instanceof RateLimitError) {
      res.setHeader('Retry-After', err.retryAfter.toString());
    }
  }
  // Handle Zod validation errors
  else if (err instanceof ZodError) {
    statusCode = 422;
    response.error.code = 'VALIDATION_ERROR';
    response.error.message = 'Validation failed';
    response.error.details = {
      errors: err.errors.map((e) => ({
        path: e.path.join('.'),
        message: e.message,
      })),
    };
  }
  // Handle Prisma errors
  else if (err instanceof Prisma.PrismaClientKnownRequestError) {
    const prismaErr = err as Prisma.PrismaClientKnownRequestError;
    switch (prismaErr.code) {
      case 'P2002':
        statusCode = 409;
        response.error.code = 'DUPLICATE_ENTRY';
        response.error.message = 'A record with this value already exists';
        break;
      case 'P2025':
        statusCode = 404;
        response.error.code = 'NOT_FOUND';
        response.error.message = 'Record not found';
        break;
      case 'P2003':
        statusCode = 400;
        response.error.code = 'FOREIGN_KEY_VIOLATION';
        response.error.message = 'Related record not found';
        break;
      default:
        response.error.code = 'DATABASE_ERROR';
        response.error.message = 'Database operation failed';
    }
  }
  // Handle Prisma validation errors
  else if (err instanceof Prisma.PrismaClientValidationError) {
    statusCode = 400;
    response.error.code = 'VALIDATION_ERROR';
    response.error.message = 'Invalid data provided';
  }
  // Handle JWT errors
  else if (err.name === 'JsonWebTokenError') {
    statusCode = 401;
    response.error.code = 'INVALID_TOKEN';
    response.error.message = 'Invalid authentication token';
  }
  else if (err.name === 'TokenExpiredError') {
    statusCode = 401;
    response.error.code = 'TOKEN_EXPIRED';
    response.error.message = 'Authentication token has expired';
  }
  // Handle syntax errors (malformed JSON)
  else if (err instanceof SyntaxError && 'body' in err) {
    statusCode = 400;
    response.error.code = 'INVALID_JSON';
    response.error.message = 'Invalid JSON in request body';
  }

  // Include stack trace in development
  if (process.env.NODE_ENV === 'development') {
    response.error.stack = err.stack;
  }

  res.status(statusCode).json(response);
};
