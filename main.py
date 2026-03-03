import json
import datetime
import logging
import bcrypt # You need this for the hashes in users.json
import sys

# --- 1. SET UP AUDIT LOGGER (Accounting) ---
audit_logger = logging.getLogger('audit_monitor')
audit_handler = logging.FileHandler('audit.log')
audit_formatter = logging.Formatter('%(asctime)s - SECURITY - %(message)s')
audit_handler.setFormatter(audit_formatter)
audit_logger.addHandler(audit_handler)
audit_logger.setLevel(logging.INFO)

def load_users():
    with open("users.json", "r") as file:
        return json.load(file)["users"]

def load_roles():
    with open("roles.json", "r") as file:
        return json.load(file)["roles"]

# --- 2. SECURE AUTHENTICATION ---
def authenticate(username, password, users):
    for user in users:
        if user["username"] == username:
            # Convert stored string hash and input password to bytes
            stored_hash = user["password"].encode('utf-8')
            user_input = password.encode('utf-8')
            
            # Check password against hash
            if bcrypt.checkpw(user_input, stored_hash):
                audit_logger.info(f"SUCCESSFUL LOGIN: User '{username}' authenticated.")
                return user["role"]
            else:
                audit_logger.warning(f"FAILED LOGIN: Incorrect password for user '{username}'.")
                return None
    
    audit_logger.warning(f"FAILED LOGIN: Attempt with non-existent username '{username}'.")
    return None
def security_audit(port):
    # A+ Senior Logic: Identifying insecure protocols
    insecure_ports = {23: "Telnet", 80: "HTTP"}
    
    if port in insecure_ports:
        print(f"CRITICAL SECURITY RISK: {insecure_ports[port]} detected on port {port}!")
        print("Shutting down to prevent unencrypted credential theft.")
        sys.exit(1) # Exit with error code
    else:
        print(f"Server starting on secure port {port}...")

# Example usage:
# security_audit(80)  # This would trigger the shutdown
security_audit(443) # This allows the app to run

def authorize(role, action, roles):
    return action in roles.get(role, [])

def log_access(username, action, result):
    # This remains for general activity tracking
    with open("access.log", "a") as log:
        timestamp = datetime.datetime.now()
        log.write(f"{timestamp} | User: {username} | Action: {action} | Result: {result}\n")

def main():
    audit_logger.info("IAM Simulator Session Started.")
    users = load_users()
    roles = load_roles()

    while True:
        username = input("\nEnter username (or type exit): ")
        if username.lower() == "exit":
            break

        password = input("Enter password: ")
        role = authenticate(username, password, users)

        if not role:
            print("Authentication Failed. Details recorded in audit.log.")
            log_access(username, "N/A", "Auth Failed")
            continue

        print(f"Login Successful! Your role is: {role}")
        action = input("Enter action (read/write/delete): ")
        
        if authorize(role, action, roles):
            print("Access Granted")
            log_access(username, action, "Granted")
        else:
            print("Access Denied")
            log_access(username, action, "Denied")

if __name__ == "__main__":
    main()