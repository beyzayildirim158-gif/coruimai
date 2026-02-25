-- Instagram AI Management System
-- Initial Database Migration

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================
-- ENUMS
-- ============================================

CREATE TYPE subscription_tier AS ENUM ('STARTER', 'PROFESSIONAL', 'PREMIUM', 'ENTERPRISE');
CREATE TYPE subscription_status AS ENUM ('ACTIVE', 'CANCELLED', 'PAST_DUE', 'TRIALING', 'PAUSED');
CREATE TYPE analysis_status AS ENUM ('PENDING', 'PROCESSING', 'COMPLETED', 'FAILED', 'CANCELLED');
CREATE TYPE report_type AS ENUM ('FULL', 'SUMMARY', 'EXECUTIVE');
CREATE TYPE payment_status AS ENUM ('PENDING', 'SUCCEEDED', 'FAILED', 'REFUNDED');

-- ============================================
-- USERS TABLE
-- ============================================

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    avatar_url TEXT,
    email_verified BOOLEAN DEFAULT FALSE,
    email_verification_token VARCHAR(255),
    password_reset_token VARCHAR(255),
    password_reset_expires TIMESTAMP WITH TIME ZONE,
    
    -- Subscription
    subscription_tier subscription_tier DEFAULT 'STARTER',
    subscription_status subscription_status DEFAULT 'ACTIVE',
    stripe_customer_id VARCHAR(255) UNIQUE,
    stripe_subscription_id VARCHAR(255) UNIQUE,
    trial_ends_at TIMESTAMP WITH TIME ZONE,
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_login_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_stripe_customer_id ON users(stripe_customer_id);

-- ============================================
-- REFRESH TOKENS TABLE
-- ============================================

CREATE TABLE refresh_tokens (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    token VARCHAR(500) UNIQUE NOT NULL,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    revoked_at TIMESTAMP WITH TIME ZONE,
    ip_address VARCHAR(45),
    user_agent TEXT
);

CREATE INDEX idx_refresh_tokens_user_id ON refresh_tokens(user_id);
CREATE INDEX idx_refresh_tokens_token ON refresh_tokens(token);

-- ============================================
-- INSTAGRAM ACCOUNTS TABLE
-- ============================================

CREATE TABLE instagram_accounts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    username VARCHAR(255) NOT NULL,
    
    -- Account Data
    followers INTEGER DEFAULT 0,
    following INTEGER DEFAULT 0,
    posts INTEGER DEFAULT 0,
    bio TEXT,
    profile_pic_url TEXT,
    profile_pic_data TEXT,
    is_verified BOOLEAN DEFAULT FALSE,
    is_private BOOLEAN DEFAULT FALSE,
    is_business BOOLEAN DEFAULT FALSE,
    
    -- Metrics
    engagement_rate DECIMAL(5, 2),
    avg_likes DECIMAL(12, 2),
    avg_comments DECIMAL(12, 2),
    bot_score DECIMAL(5, 2),
    
    -- Extended Data
    account_data JSONB,
    
    -- Tracking
    analysis_count INTEGER DEFAULT 0,
    last_analyzed_at TIMESTAMP WITH TIME ZONE,
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    UNIQUE(user_id, username)
);

CREATE INDEX idx_instagram_accounts_username ON instagram_accounts(username);
CREATE INDEX idx_instagram_accounts_user_id ON instagram_accounts(user_id);

-- ============================================
-- ANALYSES TABLE
-- ============================================

CREATE TABLE analyses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    account_id UUID NOT NULL REFERENCES instagram_accounts(id) ON DELETE CASCADE,
    
    -- Status
    status analysis_status DEFAULT 'PENDING',
    progress INTEGER DEFAULT 0 CHECK (progress >= 0 AND progress <= 100),
    current_agent VARCHAR(100),
    error_message TEXT,
    
    -- Results
    agent_results JSONB,
    
    -- Summary
    overall_score DECIMAL(5, 2) CHECK (overall_score >= 0 AND overall_score <= 100),
    score_grade CHAR(1) CHECK (score_grade IN ('A', 'B', 'C', 'D', 'F')),
    recommendations JSONB,
    
    -- Timestamps
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_analyses_user_id ON analyses(user_id);
CREATE INDEX idx_analyses_account_id ON analyses(account_id);
CREATE INDEX idx_analyses_status ON analyses(status);
CREATE INDEX idx_analyses_created_at ON analyses(created_at DESC);

-- ============================================
-- REPORTS TABLE
-- ============================================

CREATE TABLE reports (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    analysis_id UUID NOT NULL REFERENCES analyses(id) ON DELETE CASCADE,
    
    -- PDF Details
    pdf_url TEXT,
    s3_key VARCHAR(500),
    file_size INTEGER,
    report_type report_type DEFAULT 'FULL',
    
    -- Metadata
    page_count INTEGER,
    is_watermarked BOOLEAN DEFAULT FALSE,
    
    -- Timestamps
    generated_at TIMESTAMP WITH TIME ZONE,
    expires_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_reports_user_id ON reports(user_id);
CREATE INDEX idx_reports_analysis_id ON reports(analysis_id);

-- ============================================
-- PAYMENTS TABLE
-- ============================================

CREATE TABLE payments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- Stripe Data
    stripe_payment_id VARCHAR(255) UNIQUE,
    stripe_invoice_id VARCHAR(255),
    
    -- Payment Details
    amount INTEGER NOT NULL,
    currency VARCHAR(3) DEFAULT 'usd',
    status payment_status DEFAULT 'PENDING',
    plan_type subscription_tier NOT NULL,
    
    -- Metadata
    description TEXT,
    receipt_url TEXT,
    
    -- Timestamps
    paid_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_payments_user_id ON payments(user_id);
CREATE INDEX idx_payments_stripe_payment_id ON payments(stripe_payment_id);
CREATE INDEX idx_payments_created_at ON payments(created_at DESC);

-- ============================================
-- API USAGE TABLE
-- ============================================

CREATE TABLE api_usage (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- Usage Data
    endpoint VARCHAR(255) NOT NULL,
    method VARCHAR(10) NOT NULL,
    requests_count INTEGER DEFAULT 1,
    date DATE NOT NULL,
    
    -- Rate Limiting
    analyses_used INTEGER DEFAULT 0,
    month_year VARCHAR(7) NOT NULL, -- "2024-01" format
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    UNIQUE(user_id, month_year)
);

CREATE INDEX idx_api_usage_user_id ON api_usage(user_id);
CREATE INDEX idx_api_usage_date ON api_usage(date);
CREATE INDEX idx_api_usage_month_year ON api_usage(month_year);

-- ============================================
-- UPDATE TIMESTAMP FUNCTION
-- ============================================

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply update triggers
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_instagram_accounts_updated_at BEFORE UPDATE ON instagram_accounts
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_analyses_updated_at BEFORE UPDATE ON analyses
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_api_usage_updated_at BEFORE UPDATE ON api_usage
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
