#!/bin/bash
# A+ Senior Logic: Layer 4 Security Hardening

echo "Applying IAM Server Security Policy..."

# 1. Flush existing rules to start fresh
iptables -F

# 2. Allow Loopback (Localhost needs to talk to itself)
iptables -A INPUT -i lo -j ACCEPT

# 3. Allow SSH (Port 22) - Essential for remote management
iptables -A INPUT -p tcp --dport 22 -j ACCEPT

# 4. Allow HTTPS (Port 443) - For your Secure IAM Portal
iptables -A INPUT -p tcp --dport 443 -j ACCEPT

# 5. BLOCK Telnet (Port 23) and HTTP (Port 80) - Your "Hardening" step
iptables -A INPUT -p tcp --dport 23 -j REJECT
iptables -A INPUT -p tcp --dport 80 -j REJECT

# 6. Default Policy: Drop everything else (The "Implicit Deny" principle)
iptables -P INPUT DROP

echo "Hardening Complete. Port 23 and 80 are now inaccessible."
