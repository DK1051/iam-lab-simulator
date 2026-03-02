import time

def monitor_audit_log():
    print("--- AI Security Monitor Active ---")
    log_file = "audit.log"
    
    # Simple Heuristic AI: Pattern Matching for Brute Force
    threshold = 3
    
    while True:
        with open(log_file, "r") as file:
            lines = file.readlines()
            # Get the last 10 events
            recent_events = lines[-10:]
            
            # Logic: Count failures for specific users
            fail_count = {}
            for event in recent_events:
                if "FAILED LOGIN" in event:
                    # Extract username from the log string
                    parts = event.split("'")
                    if len(parts) > 1:
                        username = parts[1]
                        fail_count[username] = fail_count.get(username, 0) + 1
            
            # AI Alert Trigger
            for user, count in fail_count.items():
                if count >= threshold:
                    print(f"!!! AI ALERT: Potential Brute Force Attack detected on user: {user} ({count} failures) !!!")
        
        # Scan every 10 seconds
        time.sleep(10)

if __name__ == "__main__":
    monitor_audit_log()