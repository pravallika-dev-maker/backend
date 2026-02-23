-- Run this in your Supabase SQL Editor

-- Table for Project Financials
CREATE TABLE IF NOT EXISTS project_financials (
    financial_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id VARCHAR NOT NULL,
    project_category VARCHAR NOT NULL CHECK (project_category IN ('Services', 'Marketing', 'Products')),
    monthly_billing_amount NUMERIC NOT NULL DEFAULT 0,
    billing_owner VARCHAR NOT NULL,
    billing_start_date DATE NOT NULL,
    billing_end_date DATE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table for Cost Items
CREATE TABLE IF NOT EXISTS cost_items (
    cost_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    cost_name VARCHAR NOT NULL,
    cost_category VARCHAR NOT NULL CHECK (cost_category IN ('Salary', 'Rent', 'Tools', 'Server', 'Other')),
    monthly_amount NUMERIC NOT NULL DEFAULT 0,
    owner_name VARCHAR NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Note: Ensure that these tables have Row Level Security (RLS) policies configured based on your frontend needs,
-- or simply disable RLS if you're managing authorization purely at the application level for internal admin dashboards.
-- ALTER TABLE project_financials DISABLE ROW LEVEL SECURITY;
-- ALTER TABLE cost_items DISABLE ROW LEVEL SECURITY;
