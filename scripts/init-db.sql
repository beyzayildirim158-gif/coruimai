-- Instagram AI Management System - Database Initialization
-- This script runs when PostgreSQL container starts for the first time

-- Create extensions if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE instagram_ai TO admin;
