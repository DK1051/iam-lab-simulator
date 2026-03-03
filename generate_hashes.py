import bcrypt

passwords = ["admin123", "analyst123", "guest123"]

for pw in passwords:
    hashed = bcrypt.hashpw(pw.encode(), bcrypt.gensalt())
    print(f"{pw} -> {hashed.decode()}")
