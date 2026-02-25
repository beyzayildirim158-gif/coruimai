// Application Configuration
import dotenv from 'dotenv';
import { z } from 'zod';

dotenv.config();

// Configuration schema validation
const configSchema = z.object({
  env: z.enum(['development', 'production', 'test']).default('development'),
  port: z.coerce.number().default(3001),
  
  // Database
  databaseUrl: z.string().url(),
  
  // Redis
  redisUrl: z.string(),
  
  // JWT
  jwt: z.object({
    secret: z.string().min(32),
    accessExpiry: z.string().default('15m'),
    refreshExpiry: z.string().default('7d'),
  }),
  
  // Stripe
  stripe: z.object({
    secretKey: z.string(),
    webhookSecret: z.string(),
    prices: z.object({
      starter: z.string(),
      professional: z.string(),
      premium: z.string(),
      enterprise: z.string(),
    }),
  }),
  
  // Apify - Multiple Actors
  apify: z.object({
    apiToken: z.string(),
    actorId: z.string().default('curious_coder/instagram-scraper'),
    // Profile scrapers (fallback chain)
    actorProfile1: z.string().default('curious_coder/instagram-scraper'),
    actorProfile2: z.string().default('coderx/instagram-profile-scraper-bio-posts'),
    actorProfile3: z.string().default('apify/instagram-profile-scraper'),
    // Specialized scrapers
    actorHashtag: z.string().default('apify/instagram-hashtag-scraper'),
    actorFollowers: z.string().default('apify/instagram-followers-count-scraper'),
    actorFollowing: z.string().default('louisdeconinck/instagram-following-scraper'),
    actorComments: z.string().default('louisdeconinck/instagram-comments-scraper'),
    actorStories: z.string().default('datavoyantlab/advanced-instagram-stories-scraper'),
    actorTranscript: z.string().default('sian.agency/instagram-ai-transcript-extractor'),
  }),
  
  // AWS S3
  aws: z.object({
    accessKeyId: z.string().optional(),
    secretAccessKey: z.string().optional(),
    region: z.string().default('us-east-1'),
    s3Bucket: z.string().optional(),
  }),
  
  // Email
  email: z.object({
    host: z.string().default('smtp.sendgrid.net'),
    port: z.coerce.number().default(587),
    user: z.string().optional(),
    password: z.string().optional(),
    from: z.string().email().default('noreply@instagram-ai.com'),
  }),
  
  // CORS
  cors: z.object({
    origins: z.array(z.string()).default(['http://localhost:3000']),
  }),
  
  // Agent Orchestrator
  agentOrchestrator: z.object({
    url: z.string().url().default('http://localhost:8000'),
    timeout: z.coerce.number().default(120),
  }),
  
  // PDF Generator
  pdfGenerator: z.object({
    url: z.string().url().default('http://localhost:3002'),
  }),
});

// Parse environment variables
const parseConfig = () => {
  const corsOrigins = process.env.CORS_ORIGINS?.split(',') || ['http://localhost:3000'];
  
  return configSchema.parse({
    env: process.env.NODE_ENV,
    port: process.env.PORT,
    databaseUrl: process.env.DATABASE_URL,
    redisUrl: process.env.REDIS_URL,
    jwt: {
      secret: process.env.JWT_SECRET,
      accessExpiry: process.env.JWT_ACCESS_EXPIRY,
      refreshExpiry: process.env.JWT_REFRESH_EXPIRY,
    },
    stripe: {
      secretKey: process.env.STRIPE_SECRET_KEY,
      webhookSecret: process.env.STRIPE_WEBHOOK_SECRET,
      prices: {
        starter: process.env.STRIPE_PRICE_STARTER,
        professional: process.env.STRIPE_PRICE_PROFESSIONAL,
        premium: process.env.STRIPE_PRICE_PREMIUM,
        enterprise: process.env.STRIPE_PRICE_ENTERPRISE,
      },
    },
    apify: {
      apiToken: process.env.APIFY_API_TOKEN,
      actorId: process.env.APIFY_ACTOR_ID,
      actorProfile1: process.env.APIFY_ACTOR_PROFILE_1,
      actorProfile2: process.env.APIFY_ACTOR_PROFILE_2,
      actorProfile3: process.env.APIFY_ACTOR_PROFILE_3,
      actorHashtag: process.env.APIFY_ACTOR_HASHTAG,
      actorFollowers: process.env.APIFY_ACTOR_FOLLOWERS,
      actorFollowing: process.env.APIFY_ACTOR_FOLLOWING,
      actorComments: process.env.APIFY_ACTOR_COMMENTS,
      actorStories: process.env.APIFY_ACTOR_STORIES,
      actorTranscript: process.env.APIFY_ACTOR_TRANSCRIPT,
    },
    aws: {
      accessKeyId: process.env.AWS_ACCESS_KEY_ID,
      secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
      region: process.env.AWS_REGION,
      s3Bucket: process.env.S3_BUCKET,
    },
    email: {
      host: process.env.SMTP_HOST,
      port: process.env.SMTP_PORT,
      user: process.env.SMTP_USER,
      password: process.env.SMTP_PASSWORD,
      from: process.env.EMAIL_FROM,
    },
    cors: {
      origins: corsOrigins,
    },
    agentOrchestrator: {
      url: process.env.AGENT_ORCHESTRATOR_URL,
      timeout: process.env.AGENT_TIMEOUT_SECONDS,
    },
    pdfGenerator: {
      url: process.env.PDF_GENERATOR_URL,
    },
  });
};

export const config = parseConfig();

// Subscription tier limits
export const tierLimits = {
  STARTER: {
    analysesPerMonth: 10,
    requestsPerHour: 5,
    agents: ['systemGovernor', 'growthVirality', 'communityLoyalty'],
    agentCount: 3,
    features: {
      pdfReports: true,
      brandedReports: false,
      whiteLabelReports: false,
      apiAccess: false,
      botDetection: false,
    },
  },
  PROFESSIONAL: {
    analysesPerMonth: 50,
    requestsPerHour: 20,
    agents: ['systemGovernor', 'growthVirality', 'communityLoyalty', 'attentionArchitect', 'salesConversion'],
    agentCount: 5,
    features: {
      pdfReports: true,
      brandedReports: true,
      whiteLabelReports: false,
      apiAccess: false,
      botDetection: true,
    },
  },
  PREMIUM: {
    analysesPerMonth: 200,
    requestsPerHour: 50,
    agents: ['systemGovernor', 'growthVirality', 'communityLoyalty', 'attentionArchitect', 'salesConversion', 'visualBrand', 'domainMaster'],
    agentCount: 7,
    features: {
      pdfReports: true,
      brandedReports: true,
      whiteLabelReports: true,
      apiAccess: true,
      botDetection: true,
    },
  },
  ENTERPRISE: {
    analysesPerMonth: -1, // unlimited
    requestsPerHour: 100,
    agents: ['systemGovernor', 'growthVirality', 'communityLoyalty', 'attentionArchitect', 'salesConversion', 'visualBrand', 'domainMaster'],
    agentCount: 7,
    features: {
      pdfReports: true,
      brandedReports: true,
      whiteLabelReports: true,
      apiAccess: true,
      botDetection: true,
      customAgents: true,
      multiUser: true,
    },
  },
} as const;

export type SubscriptionTier = keyof typeof tierLimits;
