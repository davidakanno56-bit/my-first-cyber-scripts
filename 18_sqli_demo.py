import sqlite3

# Setup in-memory database with admin user
conn = sqlite3.connect(":memory:")
cursor = conn.cursor()
cursor.execute("CREATE TABLE users (id INT, username TEXT, password TEXT)")
cursor.execute("INSERT INTO users VALUES (1, 'admin', 'SuperSecretPass123')")
conn.commit()

# Attacker's malicious input string
malicious_input = "' OR '1'='1"

print("=" * 60)
print(f"[!] ATTACK INPUT TRICK: {malicious_input}")
print("=" * 60)

# -------------------------------------------------------------
# ❌ VULNERABLE DEMO (Direct String Concatenation)
# -------------------------------------------------------------
vulnerable_query = f"SELECT * FROM users WHERE username = '{malicious_input}'"
print(f"\n[1] Executing Insecure Query:\n    {vulnerable_query}")

cursor.execute(vulnerable_query)
result = cursor.fetchall()

if result:
    print("    🚨 EXPLOITED! Hacker bypassed login without password!")
    print(f"    Dumped Data: {result}")
else:
    print("    [+] Access Denied.")

# -------------------------------------------------------------
# ✅ SECURE DEMO (Parameterized Query)
# -------------------------------------------------------------
print("\n[2] Executing Secure Parameterized Query:")

secure_query = "SELECT * FROM users WHERE username = ?"
cursor.execute(secure_query, (malicious_input,))
secure_result = cursor.fetchall()

if secure_result:
    print("    🚨 EXPLOITED!")
else:
    print("    ✅ SECURE! Database treated malicious input strictly as text.")
    print("    [+] Access Denied.")

conn.close()