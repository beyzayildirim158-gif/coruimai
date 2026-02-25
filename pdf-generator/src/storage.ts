import fs from 'node:fs/promises';
import path from 'node:path';
import { S3Client, PutObjectCommand } from '@aws-sdk/client-s3';
import { config } from './config.js';
import { logger } from './logger.js';

const localDir = config.storageDir;

// Only create S3 client if valid (non-placeholder) credentials are provided
const hasValidS3Config = 
  config.aws.bucket && 
  config.aws.accessKeyId && 
  config.aws.secretAccessKey &&
  config.aws.accessKeyId !== 'placeholder' &&
  config.aws.secretAccessKey !== 'placeholder' &&
  !config.aws.accessKeyId.includes('PLACEHOLDER') &&
  !config.aws.secretAccessKey.includes('PLACEHOLDER');

const s3Client = hasValidS3Config
  ? new S3Client({
      region: config.aws.region,
      credentials: {
        accessKeyId: config.aws.accessKeyId!,
        secretAccessKey: config.aws.secretAccessKey!,
      },
    })
  : null;

export interface SaveResult {
  pdfUrl: string;
  s3Key?: string;
}

export async function savePdf(reportId: string, buffer: Buffer): Promise<SaveResult> {
  const filename = `${reportId}.pdf`;

  if (s3Client && config.aws.bucket) {
    const key = `reports/${filename}`;
    await s3Client.send(
      new PutObjectCommand({
        Bucket: config.aws.bucket,
        Key: key,
        Body: buffer,
        ContentType: 'application/pdf',
      })
    );

    const pdfUrl = `https://${config.aws.bucket}.s3.${config.aws.region}.amazonaws.com/${key}`;
    logger.info({ key }, 'Stored report in S3');
    return { pdfUrl, s3Key: key };
  }

  await fs.mkdir(localDir, { recursive: true });
  const filePath = path.join(localDir, filename);
  await fs.writeFile(filePath, buffer);

  const pdfUrl = `${config.publicUrl.replace(/\/$/, '')}/reports/${filename}`;
  logger.info({ filePath }, 'Stored report on local disk');
  return { pdfUrl, s3Key: undefined };
}
