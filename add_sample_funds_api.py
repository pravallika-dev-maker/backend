import urllib.request
import json

SUPABASE_URL = "https://yibpjemrwzawgxdcnmsw.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InlpYnBqZW1yd3phd2d4ZGNubXN3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzA1OTEzMjMsImV4cCI6MjA4NjE2NzMyM30.06Sfyeq2iGJQ_C9aXvQVgvjUBUuu2yVOFW63jMwG_i8"

sample_funds = [
    {
        "investor_name": "Phoenix Ventures",
        "amount_raised": 15000000,
        "funding_date": "2024-01-15",
        "funding_type": "Equity",
        "owner_responsible": "Pravas",
        "notes": "Series A Funding Round"
    },
    {
        "investor_name": "Global Insight Partners",
        "amount_raised": 7500000,
        "funding_date": "2024-05-10",
        "funding_type": "Debt",
        "owner_responsible": "Pravas",
        "notes": "Convertible Note"
    },
    {
        "investor_name": "Angel Network Alpha",
        "amount_raised": 2500000,
        "funding_date": "2024-08-22",
        "funding_type": "Equity",
        "owner_responsible": "Pravas",
        "notes": "Seed Extension"
    }
]

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal"
}

def insert_fund(fund):
    url = f"{SUPABASE_URL}/rest/v1/funds"
    data = json.dumps(fund).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            print(f"  Inserted: {fund['investor_name']} - Status {response.status}")
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"  Error inserting {fund['investor_name']}: HTTP {e.code} - {body}")
    except Exception as e:
        print(f"  Connection error: {e}")

if __name__ == "__main__":
    print("Attempting to insert sample fund records via Supabase REST API...")
    for fund in sample_funds:
        insert_fund(fund)
    print("\nDone. Please refresh the Funds tab in your dashboard.")
