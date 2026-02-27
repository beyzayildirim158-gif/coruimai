// Instagram AI Management System - Main Entry Point
import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import morgan from 'morgan';
import cookieParser from 'cookie-parser';
import { createServer } from 'http';
import { WebSocketServer } from 'ws';
import swaggerUi from 'swagger-ui-express';

import { config } from './config/index.js';
import { logger } from './utils/logger.js';
import { prisma } from './config/database.js';
import { redis } from './config/redis.js';
import { errorHandler } from './middleware/errorHandler.js';
import { notFoundHandler } from './middleware/notFoundHandler.js';
import { swaggerSpec } from './config/swagger.js';

// Routes
import authRoutes from './routes/auth.routes.js';
import userRoutes from './routes/user.routes.js';
import analysisRoutes from './routes/analysis.routes.js';
import reportRoutes from './routes/report.routes.js';
import paymentRoutes from './routes/payment.routes.js';
import usageRoutes from './routes/usage.routes.js';
import webhookRoutes from './routes/webhook.routes.js';
import proxyRoutes from './routes/proxy.routes.js';
import adminRoutes from './routes/admin.routes.js';

// WebSocket handler
import { setupWebSocket } from './websocket/index.js';

const app = express();
const server = createServer(app);

// WebSocket setup
const wss = new WebSocketServer({ server, path: '/ws' });
setupWebSocket(wss);

// Security middleware
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      scriptSrc: ["'self'"],
      imgSrc: ["'self'", 'data:', 'https:'],
    },
  },
}));

// CORS configuration - allow all origins in development
app.use(cors({
  origin: config.env === 'development' ? true : config.cors.origins,
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization', 'X-Request-ID'],
}));

// Request logging
app.use(morgan('combined', {
  stream: { write: (message) => logger.http(message.trim()) },
  skip: () => config.env === 'test',
}));

// Body parsing - Stripe webhook needs raw body
app.use('/api/webhooks/stripe', express.raw({ type: 'application/json' }));
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));

// Cookie parser for refresh tokens
app.use(cookieParser());

// Health check
app.get('/health', async (req, res) => {
  try {
    await prisma.$queryRaw`SELECT 1`;
    const redisStatus = redis ? await redis.ping() : 'memory-fallback';
    res.json({
      status: 'healthy',
      timestamp: new Date().toISOString(),
      services: {
        database: 'connected',
        redis: redis ? 'connected' : 'memory-fallback',
      },
    });
  } catch (error) {
    res.status(503).json({
      status: 'unhealthy',
      timestamp: new Date().toISOString(),
      error: error instanceof Error ? error.message : 'Unknown error',
    });
  }
});

// Root path - API info
app.get('/', (req, res) => {
  res.json({
    name: 'Instagram AI Management System API',
    version: '1.0.0',
    docs: '/api-docs',
    health: '/health',
  });
});

// Favicon handler - prevent 404 errors
app.get('/favicon.ico', (req, res) => {
  res.status(204).end();
});

// API Documentation
app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerSpec, {
  customCss: '.swagger-ui .topbar { display: none }',
  customSiteTitle: 'Instagram AI API Documentation',
}));
app.get('/api-docs/openapi.json', (req, res) => {
  res.json(swaggerSpec);
});

// API Routes
app.use('/api/auth', authRoutes);
app.use('/api/users', userRoutes);
app.use('/api/analyze', analysisRoutes);
app.use('/api/reports', reportRoutes);
app.use('/api/payments', paymentRoutes);
app.use('/api/usage', usageRoutes);
app.use('/api/webhooks', webhookRoutes);
app.use('/api/proxy', proxyRoutes);
app.use('/api/admin', adminRoutes);

// Error handlers
app.use(notFoundHandler);
app.use(errorHandler);

// Graceful shutdown
const gracefulShutdown = async (signal: string) => {
  logger.info(`${signal} received. Starting graceful shutdown...`);
  
  server.close(async () => {
    logger.info('HTTP server closed');
    
    await prisma.$disconnect();
    logger.info('Database connection closed');
    
    if (redis) {
      await redis.quit();
      logger.info('Redis connection closed');
    }
    
    process.exit(0);
  });
  
  // Force shutdown after 30 seconds
  setTimeout(() => {
    logger.error('Forced shutdown after timeout');
    process.exit(1);
  }, 30000);
};

process.on('SIGTERM', () => gracefulShutdown('SIGTERM'));
process.on('SIGINT', () => gracefulShutdown('SIGINT'));

// Start server
const PORT = config.port;
server.listen(PORT, () => {
  logger.info(`🚀 Server running on port ${PORT}`);
  logger.info(`📚 API Docs: http://localhost:${PORT}/api-docs`);
  logger.info(`🔌 WebSocket: ws://localhost:${PORT}/ws`);
  logger.info(`🌍 Environment: ${config.env}`);
});

export { app, server };
