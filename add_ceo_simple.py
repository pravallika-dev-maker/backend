import os
from sqlalchemy import create_engine, text

# Use Supabase Pooler connection
DATABASE_URL = "postgresql://postgres.yibpjemrwzawgxdcnmsw:QTFoSloCe0UxEomc@aws-1-ap-south-1.pooler.supabase.com:6543/postgres"

print("Connecting to Supabase...")

# Create engine with SSL
engine = create_engine(
    DATABASE_URL,
    connect_args={"sslmode": "require"},
    pool_pre_ping=True
)

# CEO user details
email = "vijay@vriksha.ai"
full_name = "Vijay"
password = "vijay@123"
can_add_users = True

print(f"Adding CEO user: {email}")

try:
    with engine.connect() as conn:
        # Check if user exists
        check_query = text("SELECT email FROM authorized_users WHERE email = :email")
        result = conn.execute(check_query, {"email": email})
        existing_user = result.fetchone()
        
        if existing_user:
            print(f"User exists. Updating...")
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
            print(f"✅ Updated!")
        else:
            print(f"Creating new user...")
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
            print(f"✅ Created!")
        
        print(f"\n✨ Done! Login with:")
        print(f"   Email: {email}")
        print(f"   Password: {password}")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
