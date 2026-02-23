-- Run this in your Supabase SQL Editor to add the project_category column to the projects table
ALTER TABLE projects ADD COLUMN IF NOT EXISTS project_category VARCHAR;
Modify the existing "Finance Overview" page to support CEO-level financial tracking.

Do NOT create a new page.
Update the current layout, calculations and ownership display according to the following rules.

------------------------------------------------
DATA SOURCES (Use existing tables)
------------------------------------------------

1) project_financials
- project_id
- project_category
- monthly_billing_amount
- billing_owner
- billing_start_date
- billing_end_date

2) cost_items
- cost_name
- cost_category (Salary / Rent / Tools / Server / Other)
- monthly_amount
- owner_name
- start_date
- end_date

------------------------------------------------
REQUIRED CHANGES
------------------------------------------------

1) REMOVE GLOBAL OWNERS LIST
The Finance Overview must NOT show all project owners.

Instead:
- Revenue section must show billing_owner
- Cost section must show owner_name

------------------------------------------------
2) MONTH-ON-MONTH FINANCIAL VIEW
Update calculations so the dashboard shows:

- Monthly revenue projection
- Monthly cost totals
- Monthly PNL

Revenue must be calculated by spreading monthly_billing_amount across months between billing_start_date and billing_end_date.

Costs must be calculated by spreading monthly_amount across months between start_date and end_date.

------------------------------------------------
3) COST BREAKDOWN (NEW REQUIREMENT)
Add a table showing:

Cost Name
Cost Category
Owner Responsible
Monthly Amount

Examples:
Office Rent → Vijay
Tools → Sachin / Kiran
Engineering Salaries → HR-Team

------------------------------------------------
4) SALARY COST SUPPORT
Ensure cost_category = 'Salary' is included in monthly cost totals.

Salaries must be treated as recurring monthly fixed expenses.

------------------------------------------------
5) HOVER / ZOOM MONTH DETAILS
When user hovers or clicks a month:

Show popup panel with:

Revenue Breakdown:
- Project name
- Billing owner
- Monthly billing amount

Cost Breakdown:
- Cost name
- Owner responsible
- Monthly amount

PNL Summary:
Revenue - Costs

------------------------------------------------
6) PROJECT TIMELINE PROJECTION
If a project runs from Feb 1 to Jan 31:

Automatically generate revenue projection for all months in that duration.

------------------------------------------------
UI UPDATE RULES
------------------------------------------------

Keep existing layout structure but update:

Top Cards:
- Total Revenue
- Total Costs
- Net PNL

Middle Section:
- Monthly timeline bar

Bottom Section:
- Cost responsibility table

------------------------------------------------
LOGIC RULES
------------------------------------------------

- Do NOT use project_owner field in finance overview.
- billing_owner = revenue responsibility
- owner_name (from cost_items) = cost responsibility
- Finance Overview must represent financial ownership, not delivery ownership.

------------------------------------------------
OUTPUT EXPECTATION
------------------------------------------------

Update existing FinanceOverview component only.
Do NOT create new routes or pages.
Maintain existing styling while adding new calculations and breakdown logic.