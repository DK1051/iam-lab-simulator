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
            # 1. Check if account is already locked 
            if user.get("status") == "locked":
                print(f"\nCRITICAL: Account '{username}' is LOCKED. Contact Admin.")
                audit_logger.critical(f"BLOCK: Login attempt on LOCKED account: {username}")
                return None

            stored_hash = user["password"].encode('utf-8')
            user_input = password.encode('utf-8')
            
            if bcrypt.checkpw(user_input, stored_hash):
                # 2. Success: Reset failed attempts
                user["failed_attempts"] = 0
                audit_logger.info(f"SUCCESSFUL LOGIN: User '{username}' authenticated.")
                return user["role"]
            else:
                # 3. Failure: Increment and check threshold 
                user["failed_attempts"] += 1
                attempts_left = 5 - user["failed_attempts"]
                
                if user["failed_attempts"] >= 5:
                    user["status"] = "locked"
                    audit_logger.critical(f"SECURITY ALERT: Account '{username}' LOCKED due to failures.")
                    print(f"\nSECURITY ALERT: Too many failed attempts. Account '{username}' is LOCKED.")
                else:
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

def authorize(role, action, roles):
    return action in roles.get(role, [])

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
def save_users(users):
    with open("users.json", "w") as file:
        json.dump({"users": users}, file, indent=2)
# --- END SESSION COMMIT ---

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
        
        # PERSISTENCE: Save the failed_attempts or locked status immediately 
        save_users(users)

        if not role:
            # Removed the generic "Authentication Failed" print because 
            # our new authenticate() function provides specific feedback.
            continue

        print(f"Login Successful! Your role is: {role}")

        # --- MOVER PATCH TRIGGER ---
        # Allow admins to move users between departments
        if role == "admin":
            trigger_move = input("Admin: Do you need to process a 'Mover' workflow? (y/n): ")
            if trigger_move.lower() == 'y':
                target_user = input("Enter the username of the person moving: ")
                new_dept = input("Enter new department (e.g., IAM): ")
                handle_mover_transition(target_user, new_dept)
                continue # Return to start of loop after move
        # ---------------------------

        action = input("Enter action (read/write/delete/move): ")
        
        if authorize(role, action, roles):
            print("Access Granted")
            log_access(username, action, "Granted")
        else:
            print("Access Denied")
            log_access(username, action, "Denied")
if __name__ == "__main__":
    main()