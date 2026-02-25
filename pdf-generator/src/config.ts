import { z } from 'zod';
import dotenv from 'dotenv';
import path from 'node:path';

dotenv.config();

const configSchema = z.object({
  port: z.coerce.number().default(3002),
  publicUrl: z.string().default(`http://localhost:${process.env.PORT || 3002}`),
  storageDir: z.string().default(path.join(process.cwd(), 'storage', 'reports')),
  aws: z.object({
    bucket: z.string().optional(),
    region: z.string().default('us-east-1'),
    accessKeyId: z.string().optional(),
    secretAccessKey: z.string().optional(),
  }),
});

export const config = configSchema.parse({
  port: process.env.PORT,
  publicUrl: process.env.PUBLIC_URL,
  storageDir: process.env.LOCAL_STORAGE_DIR,
  aws: {
    bucket: process.env.S3_BUCKET,
    region: process.env.AWS_REGION,
    accessKeyId: process.env.AWS_ACCESS_KEY_ID,
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
  },
});
