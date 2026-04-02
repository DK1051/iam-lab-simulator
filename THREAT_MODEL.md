# Threat Model — IAM Lab Simulator

## Section 1: Attacks This Project Defends Against

### Brute Force Authentication
**Threat:** An attacker repeatedly guesses passwords to gain unauthorized access.
**Control:** Adaptive lockout policy automatically locks accounts after 5 failed 
attempts. All lockout events are timestamped and recorded in audit.log for 
forensic analysis.

### SQL Injection
**Threat:** An attacker injects malicious SQL code through input fields to 
manipulate or extract database contents.
**Control:** All database interactions use parameterized queries with `?` 
placeholders. A column whitelist (`ALLOWED_COLUMNS`) prevents unauthorized 
fields from being targeted, even internally.

### Account Enumeration
**Threat:** An attacker probes the system with common usernames to identify 
valid accounts before launching a targeted attack.
**Control:** A regex-based input validation layer (the "Shield") blocks 
malformed or suspicious usernames before they reach the authentication logic. 
All rejected inputs are logged with timestamps.

### Ghost Accounts
**Threat:** Former employees retain active credentials after leaving, creating 
unauthorized access vectors.
**Control:** The Leaver workflow instantly disables accounts via a single 
database update, preventing ghost accounts from persisting in the system.

### Credential Theft via Password Leaks
**Threat:** An attacker gains access to the database and extracts passwords.
**Control:** All passwords are hashed using bcrypt with per-user salts, 
rendering stolen hashes uncrackable via rainbow table attacks.


## Section 2: Known Limitations

### No Multi-Factor Authentication (MFA)
The current system relies solely on password-based authentication. A stolen 
password is sufficient to gain access. MFA (such as TOTP or SMS verification) 
is planned for Phase 2 via Okta/Auth0 integration.

### Single-Node SQLite Database
SQLite is a file-based database running on a single machine. If the host 
machine fails or is stolen, the entire identity store becomes unavailable or 
compromised. This is not suitable for production environments requiring 
High Availability (HA) across multiple servers.

### Hardcoded Dashboard Credentials
The SOC dashboard password is currently stored as a hardcoded string in 
dashboard.py. In a production environment this would be managed via a secrets 
manager such as AWS Secrets Manager or HashiCorp Vault — never committed 
to source code.

### No Endpoint Protection
The application currently runs on a local development machine. Physical theft 
of the device would expose the SQLite database, audit logs, and application 
code. A production deployment would require full-disk encryption, remote wipe 
capability, and cloud-hosted infrastructure.

### No Network-Layer Authentication
The application has no TLS certificate, no API gateway, and no WAF (Web 
Application Firewall). All controls are application-layer only. A production 
deployment would sit behind a reverse proxy such as NGINX with HTTPS enforced.

## Section 3: Scaling to 10,000 Users

The current architecture is a intentional single-node prototype designed to 
demonstrate IAM concepts. A production deployment serving 10,000+ identities 
would require the following changes:

### Database
Replace SQLite with **PostgreSQL** hosted on a managed cloud service (AWS RDS 
or Google Cloud SQL). PostgreSQL supports concurrent connections, row-level 
locking, and automated backups — none of which SQLite provides.

### Session Management
Add **Redis** as an in-memory session store. This allows multiple application 
servers to share session state, enabling horizontal scaling without users 
being logged out when traffic is redistributed.

### Audit Log Pipeline
Replace the flat audit.log file with a **SIEM integration** (Splunk or 
Elastic Stack). At 10,000 users, a text file becomes unmanageable — a SIEM 
enables real-time alerting, correlation rules, and compliance reporting 
(SOC 2, ISO 27001).

### Identity Provisioning
Replace manual account creation with **SCIM (System for Cross-domain Identity 
Management)**. SCIM is the industry standard protocol for automatically 
provisioning and deprovisioning users from an Identity Provider (Okta, Azure AD) 
into downstream applications — eliminating the manual Joiner/Leaver process 
entirely.

### High Availability
Deploy across a minimum of **three availability zones** on a cloud provider. 
A load balancer distributes traffic across application instances, ensuring 
the dashboard and authentication service remain available if a single server 
fails. This directly addresses the risk of single-point-of-failure on a 
local machine.

### Secret Management
Move all credentials (database passwords, API keys, dashboard passwords) into 
**AWS Secrets Manager or HashiCorp Vault**. Secrets are injected at runtime 
and never stored in source code or environment files.