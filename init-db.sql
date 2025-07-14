-- PostgreSQL Database Initialization Script
-- This script runs when the PostgreSQL container starts for the first time

-- Create database if not exists (already created by POSTGRES_DB environment variable)
-- CREATE DATABASE aroma_app_db;

-- Connect to the database
\c aroma_app_db;

-- Create extensions if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create tables (these will be created by SQLAlchemy, but we can add custom indexes here)
-- The actual table creation is handled by Flask-SQLAlchemy

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE aroma_app_db TO pyme_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO pyme_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO pyme_user;

-- Set default privileges for future tables
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO pyme_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO pyme_user;

-- Log the initialization
\echo 'PostgreSQL database initialization completed for aroma_app_db' 