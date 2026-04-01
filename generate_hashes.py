# Run once to generate bcrypt hashes for initial setup.
# Replace placeholders with real values.
# NEVER commit with real passwords.

import bcrypt

passwords = ["<ADMIN_PASSWORD>", "<ANALYST_PASSWORD>", "<GUEST_PASSWORD>"]

for pw in passwords:
    hashed = bcrypt.hashpw(pw.encode(), bcrypt.gensalt())
    print(f"{pw} -> {hashed.decode()}")
