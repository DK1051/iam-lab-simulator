import json
import datetime
import logging
import bcrypt 
import sys
import re
import sqlite3
import logging

# This sets up a file that appends new events at the bottom
logging.basicConfig(
    filename='audit.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# --- 1. SET UP AUDIT LOGGER (Accounting) ---
audit_logger = logging.getLogger('audit_monitor')
audit_handler = logging.FileHandler('audit.log')
audit_formatter = logging.Formatter('%(asctime)s - SECURITY - %(message)s')
audit_handler.setFormatter(audit_formatter)
audit_logger.addHandler(audit_handler)
audit_logger.setLevel(logging.INFO)

# --- 2. DATABASE UTILITIES ---
def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row 
    return conn

def load_users():
    """Fetches all users from SQL. Replaces JSON loading."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return users
ALLOWED_COLUMNS = {"failed_attempts", "status", "role"}
def update_user_db(username, updates):
    """Updates specific fields in the DB using parameterized queries."""
    conn = get_db_connection()
    cursor = conn.cursor()
    for key, value in updates.items():
        if key not in ALLOWED_COLUMNS:
            audit_logger.critical(f"SECURITY: Blocked unauthorized column update: {key}")
            raise ValueError(f"Unauthorized column: {key}")
        # Using ? placeholders to prevent SQL Injection
        cursor.execute(f"UPDATE users SET {key} = ? WHERE username = ?", (value, username))
    conn.commit()
    conn.close()

# --- 3. DATA & VALIDATION ---
def load_roles():
    with open("roles.json", "r") as file:
        return json.load(file)["roles"]

def is_valid_username(username):
    # Regex Shield: Ensures only alphanumeric 3-15 chars enter the system
    pattern = r"^[a-zA-Z0-9]{3,15}$"
    return bool(re.match(pattern, username))

# --- 2. SECURE AUTHENTICATION ---
def authenticate(username, password):
    # Notice we don't pass 'users' as an argument anymore; we query the DB directly
    search_name = username.lower()
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Fetch only the specific user we need
    cursor.execute("SELECT * FROM users WHERE LOWER(username) = ?", (search_name,))
    row = cursor.fetchone()
    conn.close()

    if row:
        user = dict(row)
        
        # Block Locked/Disabled accounts
        if user.get("status") in ["locked", "disabled"]:
            status_type = user.get("status").upper()
            print(f"\nCRITICAL: Account '{username}' is {status_type}. Contact Admin.")
            audit_logger.critical(f"BLOCK: Login attempt on {status_type} account: {username}")
            return None

        stored_hash = user["password_hash"].encode('utf-8')
        user_input = password.encode('utf-8')

        if bcrypt.checkpw(user_input, stored_hash):
            # SUCCESS: Reset failed attempts in DB
            update_user_db(user['username'], {'failed_attempts': 0})
            audit_logger.info(f"SUCCESSFUL LOGIN: User '{username}' authenticated.")
            return user["role"]
        else:
            # FAILURE: Increment attempts
            new_attempts = user["failed_attempts"] + 1
            attempts_left = 5 - new_attempts
            
            if new_attempts >= 5:
                # LOCKOUT: Update status in DB
                update_user_db(user['username'], {'failed_attempts': new_attempts, 'status': 'locked'})
                audit_logger.critical(f"SECURITY ALERT: Account '{username}' LOCKED.")
                print(f"\nSECURITY ALERT: Too many failed attempts. Account '{username}' is LOCKED.")
            else:
                # INCORRECT PASS: Update count in DB
                update_user_db(user['username'], {'failed_attempts': new_attempts})
                audit_logger.warning(f"FAILED LOGIN: {username}. Attempts remaining: {attempts_left}")
                print(f"Invalid Password. {attempts_left} attempts remaining.")
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

def unlock_user(username):
    """Resets failed attempts and sets status to active in SQLite."""
    update_user_db(username, {"failed_attempts": 0, "status": "active"})
    print(f"🔓 User '{username}' has been reactivated in the database.")
    audit_logger.info(f"ADMIN_ACTION: User '{username}' unlocked by administrator.")
    return True

def authorize(role_name, action, roles_data):
    # Normalize everything to lowercase to match roles.json keys
    role_name = role_name.lower()
    action = action.lower()
    
    role_info = roles_data.get(role_name)
    
    if not role_info:
        return False
    
    # Check current role perms
    if action in [p.lower() for p in role_info.get("perms", [])]:
        return True
    
    # Check inheritance
    parent_role = role_info.get("inherits_from")
    if parent_role:
        return authorize(parent_role, action, roles_data)
    
    return False
def log_access(username, action, result):
    # This remains for general activity tracking
    with open("access.log", "a") as log:
        timestamp = datetime.datetime.now()
        log.write(f"{timestamp} | User: {username} | Action: {action} | Result: {result}\n")
# --- SESSION COMMIT: MOVER PATCH (JML WORKFLOW) ---

# --- HELPER WORKERS (Required for the Mover Patch to work) ---

def revoke_legacy_permissions(username):
    # Simulates the Principle of Least Privilege: Removing old access
    audit_logger.info(f"LEAST PRIVILEGE: Stripping legacy permissions for {username}...")

def assign_permission(username, permission, level):
    # Simulates precise authorization
    audit_logger.info(f"AUTHORIZATION: {username} assigned {level} for {permission}.")

def log_governance_event(username, event, details):
    # Professional Audit Logging for Identity Governance
    audit_logger.info(f"GOVERNANCE AUDIT - {event}: {username} | {details}")


# --- THE MOVER LOGIC (Your Code) ---

def handle_mover_transition(user_id, new_department):
    """
    Automates the 'Mover' phase of the JML workflow.
    """
    # 1. THE CLEAN SLATE
    revoke_legacy_permissions(user_id)
    
    # 2. THE AUTHORIZATION GRANT
    if new_department == "IAM":
        assign_permission(user_id, "IAM_FILE_ACCESS", level="READ-ONLY")
        print(f"SUCCESS: {user_id} authorized for IAM Database (Read-Only).")
        
    # 3. LOGGING
    log_governance_event(user_id, "ROLE_CHANGE", f"Moved to {new_department}")

# --- END SESSION COMMIT ---

def main():
    audit_logger.info("IAM Simulator Session Started.")
    
    roles = load_roles()

    while True:
        # 1. Capture the username
        username = input("\nEnter username (or type exit): ").strip().lower()
        if username == "exit":
            break

        # 2. THE SHIELD (The new part)
        # This stops the script before it even asks for a password
        if not is_valid_username(username):
            print("❌ SECURITY ERROR: Invalid username format. Only alphanumeric (3-15 chars).")
            audit_logger.warning(f"INPUT_REJECTION: Blocked malicious/invalid username: {username}")
            continue 

        # 3. THE REST OF YOUR CODE (Stays exactly as it was)
        password = input("Enter password: ")
        role = authenticate(username, password)



        if not role:
            continue

        print(f"Login Successful! Your role is: {role}")

        # --- ADMINISTRATIVE GOVERNANCE DASHBOARD ---
        if role == "admin":
            print("\n--- Admin Control Panel ---")
            print("1. Process 'Mover' (Change Department)")
            print("2. Unlock User Account")
            print("3. Disable Account (Leaver)")
            print("4. Skip to Application")
            
            choice = input("Select an administrative action (1-4): ")

            if choice == "1":
                target_user = input("Enter username to move: ").strip().lower()
                new_dept = input("Enter new department (e.g., IAM): ")
                
                # 1. Update the Database
                update_user_db(target_user, {"role": new_dept})
                
                # 2. Trigger the Governance Logic (JML Workflow)
                handle_mover_transition(target_user, new_dept) 
                
                audit_logger.info(f"MOVER_ACTION: {target_user} moved to {new_dept}")
                print(f"✅ User {target_user} moved to {new_dept} in the database.")
                continue

            elif choice == "2":
                target_user = input("Enter username to unlock: ").strip().lower()
                unlock_user(target_user)
                continue

            elif choice == "3":
                target = input("Enter username to DISABLE: ").strip().lower()
                # One command to the database replaces the entire loop
                update_user_db(target, {"status": "disabled"})
                print(f"🚫 Account '{target}' has been DISABLED in the database.")
                audit_logger.warning(f"LEAVER_ACTION: Account '{target}' disabled by admin.")
                continue

            elif choice == "4":
                pass

        action = input("Enter action (read/write/delete/move): ")
        
        if authorize(role, action, roles):
            print("Access Granted")
            log_access(username, action, "Granted")
        else:
            print("Access Denied")
            log_access(username, action, "Denied")
if __name__ == "__main__":
    main()