// Swagger/OpenAPI Configuration
import swaggerJsdoc from 'swagger-jsdoc';

const options: swaggerJsdoc.Options = {
  definition: {
    openapi: '3.0.0',
    info: {
      title: 'Instagram AI Management System API',
      version: '1.0.0',
      description: `
Multi-agent Instagram analytics and strategy platform powered by 7 specialized AI agents.

## Authentication
Most endpoints require a Bearer token in the Authorization header:
\`\`\`
Authorization: Bearer <access_token>
\`\`\`

## Rate Limiting
API requests are rate-limited based on subscription tier:
- Starter: 5 requests/hour, 10 analyses/month
- Professional: 20 requests/hour, 50 analyses/month
- Premium: 50 requests/hour, 200 analyses/month
- Enterprise: 100 requests/hour, unlimited analyses

## WebSocket
Real-time updates available at \`ws://localhost:3001/ws\`
      `,
      contact: {
        name: 'API Support',
        email: 'support@instagram-ai.com',
      },
      license: {
        name: 'MIT',
        url: 'https://opensource.org/licenses/MIT',
      },
    },
    servers: [
      {
        url: 'http://localhost:3001',
        description: 'Development server',
      },
      {
        url: 'https://api.instagram-ai.com',
        description: 'Production server',
      },
    ],
    components: {
      securitySchemes: {
        bearerAuth: {
          type: 'http',
          scheme: 'bearer',
          bearerFormat: 'JWT',
        },
      },
      schemas: {
        User: {
          type: 'object',
          properties: {
            id: { type: 'string', format: 'uuid' },
            email: { type: 'string', format: 'email' },
            name: { type: 'string' },
            avatarUrl: { type: 'string', nullable: true },
            emailVerified: { type: 'boolean' },
            subscriptionTier: { 
              type: 'string', 
              enum: ['STARTER', 'PROFESSIONAL', 'PREMIUM', 'ENTERPRISE'] 
            },
            subscriptionStatus: { 
              type: 'string', 
              enum: ['ACTIVE', 'CANCELLED', 'PAST_DUE', 'TRIALING', 'PAUSED'] 
            },
            createdAt: { type: 'string', format: 'date-time' },
          },
        },
        InstagramAccount: {
          type: 'object',
          properties: {
            id: { type: 'string', format: 'uuid' },
            username: { type: 'string' },
            followers: { type: 'integer' },
            following: { type: 'integer' },
            posts: { type: 'integer' },
            bio: { type: 'string', nullable: true },
            isVerified: { type: 'boolean' },
            isPrivate: { type: 'boolean' },
            isBusiness: { type: 'boolean' },
            engagementRate: { type: 'number', nullable: true },
            avgLikes: { type: 'number', nullable: true },
            avgComments: { type: 'number', nullable: true },
            botScore: { type: 'number', nullable: true },
            analysisCount: { type: 'integer' },
            lastAnalyzedAt: { type: 'string', format: 'date-time', nullable: true },
          },
        },
        Analysis: {
          type: 'object',
          properties: {
            id: { type: 'string', format: 'uuid' },
            status: { 
              type: 'string', 
              enum: ['PENDING', 'PROCESSING', 'COMPLETED', 'FAILED', 'CANCELLED'] 
            },
            progress: { type: 'integer', minimum: 0, maximum: 100 },
            currentAgent: { type: 'string', nullable: true },
            overallScore: { type: 'number', nullable: true },
            scoreGrade: { type: 'string', nullable: true },
            agentResults: { type: 'object', nullable: true },
            recommendations: { type: 'array', items: { type: 'string' }, nullable: true },
            startedAt: { type: 'string', format: 'date-time', nullable: true },
            completedAt: { type: 'string', format: 'date-time', nullable: true },
            createdAt: { type: 'string', format: 'date-time' },
          },
        },
        Report: {
          type: 'object',
          properties: {
            id: { type: 'string', format: 'uuid' },
            pdfUrl: { type: 'string', nullable: true },
            fileSize: { type: 'integer', nullable: true },
            reportType: { type: 'string', enum: ['FULL', 'SUMMARY', 'EXECUTIVE'] },
            pageCount: { type: 'integer', nullable: true },
            isWatermarked: { type: 'boolean' },
            generatedAt: { type: 'string', format: 'date-time', nullable: true },
            createdAt: { type: 'string', format: 'date-time' },
          },
        },
        Error: {
          type: 'object',
          properties: {
            success: { type: 'boolean', example: false },
            error: {
              type: 'object',
              properties: {
                code: { type: 'string' },
                message: { type: 'string' },
                details: { type: 'object', nullable: true },
              },
            },
          },
        },
        AuthTokens: {
          type: 'object',
          properties: {
            accessToken: { type: 'string' },
            refreshToken: { type: 'string' },
            expiresIn: { type: 'integer' },
          },
        },
      },
      responses: {
        UnauthorizedError: {
          description: 'Access token is missing or invalid',
          content: {
            'application/json': {
              schema: { $ref: '#/components/schemas/Error' },
            },
          },
        },
        ForbiddenError: {
          description: 'Insufficient permissions',
          content: {
            'application/json': {
              schema: { $ref: '#/components/schemas/Error' },
            },
          },
        },
        NotFoundError: {
          description: 'Resource not found',
          content: {
            'application/json': {
              schema: { $ref: '#/components/schemas/Error' },
            },
          },
        },
        ValidationError: {
          description: 'Validation error',
          content: {
            'application/json': {
              schema: { $ref: '#/components/schemas/Error' },
            },
          },
        },
        RateLimitError: {
          description: 'Rate limit exceeded',
          content: {
            'application/json': {
              schema: { $ref: '#/components/schemas/Error' },
            },
          },
        },
      },
    },
    tags: [
      { name: 'Authentication', description: 'User authentication endpoints' },
      { name: 'Users', description: 'User management endpoints' },
      { name: 'Analysis', description: 'Instagram account analysis endpoints' },
      { name: 'Reports', description: 'PDF report generation endpoints' },
      { name: 'Payments', description: 'Subscription and payment endpoints' },
      { name: 'Usage', description: 'API usage and rate limiting endpoints' },
    ],
  },
  apis: ['./src/routes/*.ts'],
};

export const swaggerSpec = swaggerJsdoc(options);
