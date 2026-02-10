import os
from sqlalchemy import create_engine, text

# Use the same DATABASE_URL as in app/database.py
# Updated to use Pooler (port 6543) for Railway compatibility
DATABASE_URL = "postgresql://postgres.yibpjemrwzawgxdcnmsw:QTFoSloCe0UxEomc@aws-1-ap-south-1.pooler.supabase.com:6543/postgres"

print(f"Connecting to database...")

# Create engine
engine = create_engine(DATABASE_URL)

# CEO user details
email = "vijay@vriksha.ai"
full_name = "Vijay"
password = "vijay@123"  # In production, this should be hashed
can_add_users = True

try:
    with engine.connect() as conn:
        # Check if user already exists
        check_query = text("SELECT email FROM authorized_users WHERE email = :email")
        result = conn.execute(check_query, {"email": email})
        existing_user = result.fetchone()
        
        if existing_user:
            print(f"User {email} already exists. Updating...")
            update_query = text("""
                UPDATE authorized_users 
                SET full_name = :full_name, 
                    hashed_password = :password, 
                    can_add_users = :can_add_users
                WHERE email = :email
            """)
            conn.execute(update_query, {
                "email": email,
                "full_name": full_name,
                "password": password,
                "can_add_users": can_add_users
            })
            conn.commit()
            print(f"✅ CEO user {email} updated successfully!")
        else:
            print(f"Creating new CEO user {email}...")
            insert_query = text("""
                INSERT INTO authorized_users (email, full_name, hashed_password, can_add_users)
                VALUES (:email, :full_name, :password, :can_add_users)
            """)
            conn.execute(insert_query, {
                "email": email,
                "full_name": full_name,
                "password": password,
                "can_add_users": can_add_users
            })
            conn.commit()
            print(f"✅ CEO user {email} created successfully!")
        
        # Verify the user was added/updated
        verify_query = text("SELECT email, full_name, can_add_users FROM authorized_users WHERE email = :email")
        result = conn.execute(verify_query, {"email": email})
        user = result.fetchone()
        
        if user:
            print(f"\n📋 User Details:")
            print(f"   Email: {user[0]}")
            print(f"   Full Name: {user[1]}")
            print(f"   CEO Status: {user[2]}")
            print(f"   Password: {password}")
        
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)

print("\n✨ Done! You can now login with:")
print(f"   Email: {email}")
print(f"   Password: {password}")
