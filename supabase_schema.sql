-- Supabase SQL Migration Script
-- Generated from Google Sheets data
-- Run this in Supabase SQL Editor

-- 1. Drop existing tables (if any)
DROP TABLE IF EXISTS stage_history CASCADE;
DROP TABLE IF EXISTS resources CASCADE;
DROP TABLE IF EXISTS projects CASCADE;
DROP TABLE IF EXISTS stages CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- 2. Create Users Table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    full_name TEXT,
    email TEXT UNIQUE,
    hashed_password TEXT
);

-- 3. Create Stages Table
CREATE TABLE stages (
    id SERIAL PRIMARY KEY,
    stage_name TEXT,
    stage_order INTEGER
);

-- 4. Create Projects Table
CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    record_id TEXT UNIQUE,
    client_name TEXT,
    deal_type TEXT,
    deal_value FLOAT,
    project_owner_name TEXT,
    current_stage_name TEXT,
    next_stage_name TEXT,
    next_stage_expected_date TEXT,
    deal_status TEXT,
    execution_status TEXT,
    project_started_date TEXT
);

-- 5. Create Resources Table
CREATE TABLE resources (
    id SERIAL PRIMARY KEY,
    resource_name TEXT,
    role TEXT,
    assigned_record_id TEXT
);

-- 6. Create Stage History Table
CREATE TABLE stage_history (
    id SERIAL PRIMARY KEY,
    record_id TEXT,
    stage_name TEXT,
    stage_start_date TEXT,
    stage_end_date TEXT
);

-- 7. Insert Admin User
INSERT INTO users (full_name, email, hashed_password) 
VALUES ('Admin User', 'admin@example.com', 'password123');

-- Note: The actual data from Google Sheets will be inserted by running the Python migration script
-- Or you can manually insert data using the Supabase dashboard
