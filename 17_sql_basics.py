import sqlite3

# 1. Connect to an in-memory SQL database (creates a temporary database)
conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

print("[-] Creating 'users' table in SQL database...")

# 2. Create a SQL Table named 'users' with id, username, and role
cursor.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        role TEXT
    )
""")

# 3. Insert user records into the table
print("[-] Inserting sample user records...")
cursor.execute("INSERT INTO users (username, role) VALUES ('david_akanno', 'Security Analyst')")
cursor.execute("INSERT INTO users (username, role) VALUES ('admin_root', 'System Admin')")
cursor.execute("INSERT INTO users (username, role) VALUES ('guest_user', 'Guest')")

# 4. Fetch and display all users using a SQL query
print("\n[+] Querying SQL Database: SELECT * FROM users;")
cursor.execute("SELECT * FROM users")
all_users = cursor.fetchall()

print("-" * 45)
print("ID  | USERNAME        | ROLE")
print("-" * 45)
for user in all_users:
    print(f"{user[0]:<3} | {user[1]:<15} | {user[2]}")
print("-" * 45)

# Close database connection
conn.close()