/*
  Warnings:

  - The primary key for the `analyses` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - You are about to alter the column `overall_score` on the `analyses` table. The data in that column could be lost. The data in that column will be cast from `Decimal(5,2)` to `DoublePrecision`.
  - The primary key for the `api_usage` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - The primary key for the `instagram_accounts` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - You are about to alter the column `engagement_rate` on the `instagram_accounts` table. The data in that column could be lost. The data in that column will be cast from `Decimal(5,2)` to `DoublePrecision`.
  - You are about to alter the column `avg_likes` on the `instagram_accounts` table. The data in that column could be lost. The data in that column will be cast from `Decimal(12,2)` to `DoublePrecision`.
  - You are about to alter the column `avg_comments` on the `instagram_accounts` table. The data in that column could be lost. The data in that column will be cast from `Decimal(12,2)` to `DoublePrecision`.
  - You are about to alter the column `bot_score` on the `instagram_accounts` table. The data in that column could be lost. The data in that column will be cast from `Decimal(5,2)` to `DoublePrecision`.
  - The primary key for the `payments` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - The primary key for the `refresh_tokens` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - The primary key for the `reports` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - The primary key for the `users` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - Made the column `status` on table `analyses` required. This step will fail if there are existing NULL values in that column.
  - Made the column `progress` on table `analyses` required. This step will fail if there are existing NULL values in that column.
  - Made the column `created_at` on table `analyses` required. This step will fail if there are existing NULL values in that column.
  - Made the column `updated_at` on table `analyses` required. This step will fail if there are existing NULL values in that column.
  - Made the column `requests_count` on table `api_usage` required. This step will fail if there are existing NULL values in that column.
  - Made the column `analyses_used` on table `api_usage` required. This step will fail if there are existing NULL values in that column.
  - Made the column `created_at` on table `api_usage` required. This step will fail if there are existing NULL values in that column.
  - Made the column `updated_at` on table `api_usage` required. This step will fail if there are existing NULL values in that column.
  - Made the column `followers` on table `instagram_accounts` required. This step will fail if there are existing NULL values in that column.
  - Made the column `following` on table `instagram_accounts` required. This step will fail if there are existing NULL values in that column.
  - Made the column `posts` on table `instagram_accounts` required. This step will fail if there are existing NULL values in that column.
  - Made the column `is_verified` on table `instagram_accounts` required. This step will fail if there are existing NULL values in that column.
  - Made the column `is_private` on table `instagram_accounts` required. This step will fail if there are existing NULL values in that column.
  - Made the column `is_business` on table `instagram_accounts` required. This step will fail if there are existing NULL values in that column.
  - Made the column `analysis_count` on table `instagram_accounts` required. This step will fail if there are existing NULL values in that column.
  - Made the column `created_at` on table `instagram_accounts` required. This step will fail if there are existing NULL values in that column.
  - Made the column `updated_at` on table `instagram_accounts` required. This step will fail if there are existing NULL values in that column.
  - Made the column `currency` on table `payments` required. This step will fail if there are existing NULL values in that column.
  - Made the column `status` on table `payments` required. This step will fail if there are existing NULL values in that column.
  - Made the column `created_at` on table `payments` required. This step will fail if there are existing NULL values in that column.
  - Made the column `created_at` on table `refresh_tokens` required. This step will fail if there are existing NULL values in that column.
  - Made the column `report_type` on table `reports` required. This step will fail if there are existing NULL values in that column.
  - Made the column `is_watermarked` on table `reports` required. This step will fail if there are existing NULL values in that column.
  - Made the column `created_at` on table `reports` required. This step will fail if there are existing NULL values in that column.
  - Made the column `email_verified` on table `users` required. This step will fail if there are existing NULL values in that column.
  - Made the column `subscription_tier` on table `users` required. This step will fail if there are existing NULL values in that column.
  - Made the column `subscription_status` on table `users` required. This step will fail if there are existing NULL values in that column.
  - Made the column `created_at` on table `users` required. This step will fail if there are existing NULL values in that column.
  - Made the column `updated_at` on table `users` required. This step will fail if there are existing NULL values in that column.

*/
-- AlterEnum
ALTER TYPE "report_type" ADD VALUE 'CUSTOM';

-- DropForeignKey
ALTER TABLE "analyses" DROP CONSTRAINT "analyses_account_id_fkey";

-- DropForeignKey
ALTER TABLE "analyses" DROP CONSTRAINT "analyses_user_id_fkey";

-- DropForeignKey
ALTER TABLE "api_usage" DROP CONSTRAINT "api_usage_user_id_fkey";

-- DropForeignKey
ALTER TABLE "instagram_accounts" DROP CONSTRAINT "instagram_accounts_user_id_fkey";

-- DropForeignKey
ALTER TABLE "payments" DROP CONSTRAINT "payments_user_id_fkey";

-- DropForeignKey
ALTER TABLE "refresh_tokens" DROP CONSTRAINT "refresh_tokens_user_id_fkey";

-- DropForeignKey
ALTER TABLE "reports" DROP CONSTRAINT "reports_analysis_id_fkey";

-- DropForeignKey
ALTER TABLE "reports" DROP CONSTRAINT "reports_user_id_fkey";

-- DropIndex
DROP INDEX "idx_analyses_created_at";

-- DropIndex
DROP INDEX "idx_payments_created_at";

-- AlterTable
ALTER TABLE "analyses" DROP CONSTRAINT "analyses_pkey",
ALTER COLUMN "id" DROP DEFAULT,
ALTER COLUMN "id" SET DATA TYPE TEXT,
ALTER COLUMN "user_id" SET DATA TYPE TEXT,
ALTER COLUMN "account_id" SET DATA TYPE TEXT,
ALTER COLUMN "status" SET NOT NULL,
ALTER COLUMN "progress" SET NOT NULL,
ALTER COLUMN "current_agent" SET DATA TYPE TEXT,
ALTER COLUMN "overall_score" SET DATA TYPE DOUBLE PRECISION,
ALTER COLUMN "score_grade" SET DATA TYPE TEXT,
ALTER COLUMN "started_at" SET DATA TYPE TIMESTAMP(3),
ALTER COLUMN "completed_at" SET DATA TYPE TIMESTAMP(3),
ALTER COLUMN "created_at" SET NOT NULL,
ALTER COLUMN "created_at" SET DATA TYPE TIMESTAMP(3),
ALTER COLUMN "updated_at" SET NOT NULL,
ALTER COLUMN "updated_at" DROP DEFAULT,
ALTER COLUMN "updated_at" SET DATA TYPE TIMESTAMP(3),
ADD CONSTRAINT "analyses_pkey" PRIMARY KEY ("id");

-- AlterTable
ALTER TABLE "api_usage" DROP CONSTRAINT "api_usage_pkey",
ALTER COLUMN "id" DROP DEFAULT,
ALTER COLUMN "id" SET DATA TYPE TEXT,
ALTER COLUMN "user_id" SET DATA TYPE TEXT,
ALTER COLUMN "endpoint" SET DATA TYPE TEXT,
ALTER COLUMN "method" SET DATA TYPE TEXT,
ALTER COLUMN "requests_count" SET NOT NULL,
ALTER COLUMN "analyses_used" SET NOT NULL,
ALTER COLUMN "month_year" SET DATA TYPE TEXT,
ALTER COLUMN "created_at" SET NOT NULL,
ALTER COLUMN "created_at" SET DATA TYPE TIMESTAMP(3),
ALTER COLUMN "updated_at" SET NOT NULL,
ALTER COLUMN "updated_at" DROP DEFAULT,
ALTER COLUMN "updated_at" SET DATA TYPE TIMESTAMP(3),
ADD CONSTRAINT "api_usage_pkey" PRIMARY KEY ("id");

-- AlterTable
ALTER TABLE "instagram_accounts" DROP CONSTRAINT "instagram_accounts_pkey",
ALTER COLUMN "id" DROP DEFAULT,
ALTER COLUMN "id" SET DATA TYPE TEXT,
ALTER COLUMN "user_id" SET DATA TYPE TEXT,
ALTER COLUMN "username" SET DATA TYPE TEXT,
ALTER COLUMN "followers" SET NOT NULL,
ALTER COLUMN "following" SET NOT NULL,
ALTER COLUMN "posts" SET NOT NULL,
ALTER COLUMN "is_verified" SET NOT NULL,
ALTER COLUMN "is_private" SET NOT NULL,
ALTER COLUMN "is_business" SET NOT NULL,
ALTER COLUMN "engagement_rate" SET DATA TYPE DOUBLE PRECISION,
ALTER COLUMN "avg_likes" SET DATA TYPE DOUBLE PRECISION,
ALTER COLUMN "avg_comments" SET DATA TYPE DOUBLE PRECISION,
ALTER COLUMN "bot_score" SET DATA TYPE DOUBLE PRECISION,
ALTER COLUMN "analysis_count" SET NOT NULL,
ALTER COLUMN "last_analyzed_at" SET DATA TYPE TIMESTAMP(3),
ALTER COLUMN "created_at" SET NOT NULL,
ALTER COLUMN "created_at" SET DATA TYPE TIMESTAMP(3),
ALTER COLUMN "updated_at" SET NOT NULL,
ALTER COLUMN "updated_at" DROP DEFAULT,
ALTER COLUMN "updated_at" SET DATA TYPE TIMESTAMP(3),
ADD CONSTRAINT "instagram_accounts_pkey" PRIMARY KEY ("id");

-- AlterTable
ALTER TABLE "payments" DROP CONSTRAINT "payments_pkey",
ALTER COLUMN "id" DROP DEFAULT,
ALTER COLUMN "id" SET DATA TYPE TEXT,
ALTER COLUMN "user_id" SET DATA TYPE TEXT,
ALTER COLUMN "stripe_payment_id" SET DATA TYPE TEXT,
ALTER COLUMN "stripe_invoice_id" SET DATA TYPE TEXT,
ALTER COLUMN "currency" SET NOT NULL,
ALTER COLUMN "currency" SET DATA TYPE TEXT,
ALTER COLUMN "status" SET NOT NULL,
ALTER COLUMN "paid_at" SET DATA TYPE TIMESTAMP(3),
ALTER COLUMN "created_at" SET NOT NULL,
ALTER COLUMN "created_at" SET DATA TYPE TIMESTAMP(3),
ADD CONSTRAINT "payments_pkey" PRIMARY KEY ("id");

-- AlterTable
ALTER TABLE "refresh_tokens" DROP CONSTRAINT "refresh_tokens_pkey",
ALTER COLUMN "id" DROP DEFAULT,
ALTER COLUMN "id" SET DATA TYPE TEXT,
ALTER COLUMN "token" SET DATA TYPE TEXT,
ALTER COLUMN "user_id" SET DATA TYPE TEXT,
ALTER COLUMN "expires_at" SET DATA TYPE TIMESTAMP(3),
ALTER COLUMN "created_at" SET NOT NULL,
ALTER COLUMN "created_at" SET DATA TYPE TIMESTAMP(3),
ALTER COLUMN "revoked_at" SET DATA TYPE TIMESTAMP(3),
ALTER COLUMN "ip_address" SET DATA TYPE TEXT,
ADD CONSTRAINT "refresh_tokens_pkey" PRIMARY KEY ("id");

-- AlterTable
ALTER TABLE "reports" DROP CONSTRAINT "reports_pkey",
ALTER COLUMN "id" DROP DEFAULT,
ALTER COLUMN "id" SET DATA TYPE TEXT,
ALTER COLUMN "user_id" SET DATA TYPE TEXT,
ALTER COLUMN "analysis_id" SET DATA TYPE TEXT,
ALTER COLUMN "s3_key" SET DATA TYPE TEXT,
ALTER COLUMN "report_type" SET NOT NULL,
ALTER COLUMN "is_watermarked" SET NOT NULL,
ALTER COLUMN "generated_at" SET DATA TYPE TIMESTAMP(3),
ALTER COLUMN "expires_at" SET DATA TYPE TIMESTAMP(3),
ALTER COLUMN "created_at" SET NOT NULL,
ALTER COLUMN "created_at" SET DATA TYPE TIMESTAMP(3),
ADD CONSTRAINT "reports_pkey" PRIMARY KEY ("id");

-- AlterTable
ALTER TABLE "users" DROP CONSTRAINT "users_pkey",
ALTER COLUMN "id" DROP DEFAULT,
ALTER COLUMN "id" SET DATA TYPE TEXT,
ALTER COLUMN "email" SET DATA TYPE TEXT,
ALTER COLUMN "password_hash" SET DATA TYPE TEXT,
ALTER COLUMN "name" SET DATA TYPE TEXT,
ALTER COLUMN "email_verified" SET NOT NULL,
ALTER COLUMN "email_verification_token" SET DATA TYPE TEXT,
ALTER COLUMN "password_reset_token" SET DATA TYPE TEXT,
ALTER COLUMN "password_reset_expires" SET DATA TYPE TIMESTAMP(3),
ALTER COLUMN "subscription_tier" SET NOT NULL,
ALTER COLUMN "subscription_status" SET NOT NULL,
ALTER COLUMN "stripe_customer_id" SET DATA TYPE TEXT,
ALTER COLUMN "stripe_subscription_id" SET DATA TYPE TEXT,
ALTER COLUMN "trial_ends_at" SET DATA TYPE TIMESTAMP(3),
ALTER COLUMN "created_at" SET NOT NULL,
ALTER COLUMN "created_at" SET DATA TYPE TIMESTAMP(3),
ALTER COLUMN "updated_at" SET NOT NULL,
ALTER COLUMN "updated_at" DROP DEFAULT,
ALTER COLUMN "updated_at" SET DATA TYPE TIMESTAMP(3),
ALTER COLUMN "last_login_at" SET DATA TYPE TIMESTAMP(3),
ADD CONSTRAINT "users_pkey" PRIMARY KEY ("id");

-- CreateIndex
CREATE INDEX "analyses_created_at_idx" ON "analyses"("created_at");

-- CreateIndex
CREATE INDEX "payments_created_at_idx" ON "payments"("created_at");

-- AddForeignKey
ALTER TABLE "refresh_tokens" ADD CONSTRAINT "refresh_tokens_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "users"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "instagram_accounts" ADD CONSTRAINT "instagram_accounts_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "users"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "analyses" ADD CONSTRAINT "analyses_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "users"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "analyses" ADD CONSTRAINT "analyses_account_id_fkey" FOREIGN KEY ("account_id") REFERENCES "instagram_accounts"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "reports" ADD CONSTRAINT "reports_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "users"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "reports" ADD CONSTRAINT "reports_analysis_id_fkey" FOREIGN KEY ("analysis_id") REFERENCES "analyses"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "payments" ADD CONSTRAINT "payments_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "users"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "api_usage" ADD CONSTRAINT "api_usage_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "users"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- RenameIndex
ALTER INDEX "idx_analyses_account_id" RENAME TO "analyses_account_id_idx";

-- RenameIndex
ALTER INDEX "idx_analyses_status" RENAME TO "analyses_status_idx";

-- RenameIndex
ALTER INDEX "idx_analyses_user_id" RENAME TO "analyses_user_id_idx";

-- RenameIndex
ALTER INDEX "idx_api_usage_date" RENAME TO "api_usage_date_idx";

-- RenameIndex
ALTER INDEX "idx_api_usage_month_year" RENAME TO "api_usage_month_year_idx";

-- RenameIndex
ALTER INDEX "idx_api_usage_user_id" RENAME TO "api_usage_user_id_idx";

-- RenameIndex
ALTER INDEX "idx_instagram_accounts_user_id" RENAME TO "instagram_accounts_user_id_idx";

-- RenameIndex
ALTER INDEX "idx_instagram_accounts_username" RENAME TO "instagram_accounts_username_idx";

-- RenameIndex
ALTER INDEX "idx_payments_stripe_payment_id" RENAME TO "payments_stripe_payment_id_idx";

-- RenameIndex
ALTER INDEX "idx_payments_user_id" RENAME TO "payments_user_id_idx";

-- RenameIndex
ALTER INDEX "idx_refresh_tokens_token" RENAME TO "refresh_tokens_token_idx";

-- RenameIndex
ALTER INDEX "idx_refresh_tokens_user_id" RENAME TO "refresh_tokens_user_id_idx";

-- RenameIndex
ALTER INDEX "idx_reports_analysis_id" RENAME TO "reports_analysis_id_idx";

-- RenameIndex
ALTER INDEX "idx_reports_user_id" RENAME TO "reports_user_id_idx";

-- RenameIndex
ALTER INDEX "idx_users_email" RENAME TO "users_email_idx";

-- RenameIndex
ALTER INDEX "idx_users_stripe_customer_id" RENAME TO "users_stripe_customer_id_idx";
