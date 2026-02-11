
import sqlite3

conn = sqlite3.connect('sql_app.db')
cursor = conn.cursor()

print("--- USERS ---")
cursor.execute("SELECT full_name, email, access_level, can_add_users FROM users")
for row in cursor.fetchall():
    print(f"User: {row[0]}, Email: {row[1]}, Access: {row[2]}, IS_CEO: {row[3]}")

print("\n--- PROJECTS ---")
cursor.execute("SELECT client_name, record_id, project_owner_name FROM projects")
for row in cursor.fetchall():
    print(f"Project: {row[0]} (ID: {row[1]}), Owner: {row[2]}")

print("\n--- RESOURCES ---")
# Check if email/access_level columns exist first or just select * if unsure
# But based on previous schema viewing, they should exist.
try:
    cursor.execute("SELECT resource_name, email, role, access_level, assigned_record_id FROM resources")
    for row in cursor.fetchall():
        print(f"Resource: {row[0]}, Email: {row[1]}, Role: {row[2]}, Access: {row[3]}, ProjectID: {row[4]}")
except sqlite3.OperationalError as e:
    print(f"Error querying resources: {e}")
    # Fallback to select * to debug schema
    cursor.execute("PRAGMA table_info(resources)")
    columns = [t[1] for t in cursor.fetchall()]
    print(f"Resource Columns: {columns}")
    cursor.execute("SELECT * FROM resources")
    for row in cursor.fetchall():
        print(row)

conn.close()
