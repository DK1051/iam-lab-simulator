![Python](https://img.shields.io/badge/Python-3.x-blue)
![Status](https://img.shields.io/badge/Status-Active-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
# IAM RBAC System  
**Authentication • Authorization • Audit Logging (AAA Model)**

## Overview

This project simulates a simplified Identity & Access Management (IAM) system implementing core access control principles used in enterprise environments.

It demonstrates:

- Identity verification (Authentication)
- Role-based access control (Authorization)
- Activity traceability (Accounting / Audit Logging)
- Principle of Least Privilege enforcement
- Structured role-permission governance

The system is designed to model foundational IAM control logic in a controlled environment.

---

## Key Capabilities

- User authentication workflow
- Role-to-permission mapping
- Access validation before action execution
- Structured audit logging with timestamps
- Persistent CLI-based execution flow
- JSON-based identity and role data storage
- AI-Powered Threat Detection: Real-time analysis of audit logs to flag brute-force attacks

---

## Security Architecture (Current)

The system implements the **AAA Model** (Authentication, Authorization, Accounting) using industry-standard libraries:

- **Secure Authentication:** Passwords are never stored in plaintext. The system uses **salted bcrypt hashes** ($2b$12$) to ensure credential integrity.
- **Granular Accounting:** Dedicated `audit.log` tracks all security events (Successful logins, Incorrect passwords, Non-existent user attempts).
- **AI-Driven Monitoring:** Integrated an Anomaly Detector (`ai_monitor.py`) to identify Brute Force patterns in real-time using pattern recognition.

### Planned Enhancements:
- Account lockout logic (Automated status: "locked" after 5 failures).
- Role hierarchy model (Manager roles inheriting Analyst permissions).
- Transition from JSON to SQLite for structured identity data.
### Authentication
- Username/password validation
- Access gating before system interaction

### Authorization
- Role-Based Access Control (RBAC)
- Roles define permissions
- Users inherit permissions via assigned roles
- Enforces least privilege principle

### Accounting
- Logs all actions
- Captures:
  - User identity
  - Attempted action
  - Authorization result
  - Timestamp
- Maintains traceability and audit readiness

### Infrastructure & Security
- A shell-based hardening script (harden_server.sh) designed for Linux environments to secure my IAM deployment 
- Implements an Implicit Deny policy at Layer 4, specifically blocking Port 23 and Port 80 to prevent unencrypted credential theft, while permitting Port 443 and Port 22 for secure management.

---

## Security Design Considerations

Current implementation is a controlled simulation and includes identified limitations:

- Plaintext credential storage (non-production)
- No account lockout policy
- No password hashing
- No session/token management

Planned Enhancements:

- bcrypt-based password hashing
- Failed login threshold & lockout logic
- Role hierarchy model
- Token/session simulation
- Input validation hardening
- Transition to lightweight web interface

---

## Governance Model

- Centralized role definitions
- Clear separation of identity and permissions
- Explicit authorization checks before execution
- Immutable audit logging structure

---

## Technologies

- Python 3
- JSON data persistence
- Command-line interface
- Git version control

---

## Roadmap
- [x] Implement secure credential handling (Bcrypt)
- [x] Integrate AI-driven log monitoring
- [ ] Introduce role hierarchy (Manager/User inheritance)
- [ ] Add unit testing framework for Auth logic
- [ ] Transition to SQLite for structured data
- [ ] Containerize application (Docker)

---

## Author

Eojin Kim  
IAM-focused security practitioner  
Target: IAM / Security Operations roles (Canada)