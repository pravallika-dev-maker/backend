from backend.app.database import engine
from sqlalchemy import text
import sys

def set_ceo(email: str, password: str = None):
    """Sets the 'can_add_users' flag and optionally a password for the specified email."""
    with engine.connect() as conn:
        print(f"Checking for user: {email}")
        result = conn.execute(text("SELECT id FROM users WHERE email = :email"), {"email": email}).fetchone()
        
        if not result:
            print(f"Error: User with email '{email}' not found in database.")
            print("Please ensure the user exists first.")
            return

        if password:
            print(f"Updating user '{email}' with CEO status and password...")
            conn.execute(
                text("UPDATE users SET can_add_users = True, hashed_password = :password WHERE email = :email"),
                {"email": email, "password": password}
            )
        else:
            print(f"Updating user '{email}' to CEO status...")
            conn.execute(
                text("UPDATE users SET can_add_users = True WHERE email = :email"),
                {"email": email}
            )
            
        conn.commit()
        print(f"Success! {email} is now authorized with CEO privileges.")
        if password:
            print(f"Password has been set successfully.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python set_ceo.py <email> [password]")
    elif len(sys.argv) == 2:
        set_ceo(sys.argv[1])
    else:
        set_ceo(sys.argv[1], sys.argv[2])
