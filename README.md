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

---

## Architecture

```
User → Authentication → Authorization (RBAC) → Action → Audit Log
```

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

- Implement secure credential handling
- Introduce role hierarchy
- Add unit testing framework
- Containerize application (Docker)
- Deploy demonstration environment

---

## Author

Eojin Kim  
IAM-focused security practitioner  
Target: IAM / Security Operations roles (Canada)
