import { z } from 'zod';
import dotenv from 'dotenv';

dotenv.config();

const configSchema = z.object({
  port: z.coerce.number().default(4002),
  stripeSecretKey: z.string().min(1, 'STRIPE_SECRET_KEY missing'),
  stripeWebhookSecret: z.string().min(1, 'STRIPE_WEBHOOK_SECRET missing'),
  databaseUrl: z.string().url(),
});

export const config = configSchema.parse({
  port: process.env.PORT,
  stripeSecretKey: process.env.STRIPE_SECRET_KEY,
  stripeWebhookSecret: process.env.STRIPE_WEBHOOK_SECRET,
  databaseUrl: process.env.DATABASE_URL,
});
