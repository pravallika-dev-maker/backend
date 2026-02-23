-- Run this in your Supabase SQL Editor to add the contract_years column to the projects table
ALTER TABLE projects ADD COLUMN IF NOT EXISTS contract_years NUMERIC;
