
import sqlite3

db_path = 'sql_app.db'

def add_column_if_not_exists(cursor, table, column, definition):
    try:
        cursor.execute(f"SELECT {column} FROM {table} LIMIT 1")
    except sqlite3.OperationalError:
        print(f"Adding column '{column}' to table '{table}'...")
        cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column} {definition}")
        print(f"Column '{column}' added.")
    except Exception as e:
        print(f"Error checking column {column} in {table}: {e}")

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 1. Fix Users Table
    print("Checking 'users' table...")
    add_column_if_not_exists(cursor, "users", "access_level", "VARCHAR DEFAULT 'READ'")
    add_column_if_not_exists(cursor, "users", "can_add_users", "BOOLEAN DEFAULT 0")

    # 2. Fix Resources Table
    print("Checking 'resources' table...")
    # existing columns: id, resource_name, role, assigned_record_id
    # new columns: email, access_level
    add_column_if_not_exists(cursor, "resources", "email", "VARCHAR")
    add_column_if_not_exists(cursor, "resources", "access_level", "VARCHAR DEFAULT 'READ'")

    conn.commit()
    print("Database schema update completed successfully.")

    # Verify
    print("\n--- Verifying Users Schema ---")
    cursor.execute("PRAGMA table_info(users)")
    for col in cursor.fetchall():
        print(col)

    print("\n--- Verifying Resources Schema ---")
    cursor.execute("PRAGMA table_info(resources)")
    for col in cursor.fetchall():
        print(col)

    conn.close()

except Exception as e:
    print(f"An error occurred: {e}")
