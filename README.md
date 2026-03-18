![Python](https://img.shields.io/badge/Python-3.x-blue)
![Status](https://img.shields.io/badge/Status-Active-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

# Identity & Access Management (IAM) Lab Simulator v1.4

A security-focused Python application simulating a professional IAM environment. This project demonstrates the implementation of the **Joiner-Mover-Leaver (JML)** identity lifecycle, secure authentication, and database-driven access control.

## 🚀 Key Technical Features

### 1. Identity Lifecycle Management (JML)
The simulator handles the core phases of a user's lifecycle within an organization:
* **Joiner:** Automated provisioning via SQLite database migration.
* **Mover:** Administrative dashboard to change user roles. When a user moves departments, the system automatically triggers a **"Least Privilege"** audit to revoke legacy permissions.
* **Leaver:** Instant account deactivation logic that prevents "ghost accounts" from remaining active in the system.

### 2. Defensive Security Controls
* **Password Hashing:** Implements `bcrypt` with salt to protect credentials against rainbow table attacks.
* **SQL Injection Prevention:** All database interactions use **parameterized queries** (`?` placeholders) to prevent SQLi.
* **Input Sanitization (The Shield):** A Regex-based validation layer that blocks malicious or malformed usernames before they reach the authentication logic.
* **Adaptive Lockout Policy:** Automatically locks accounts after 5 failed login attempts to mitigate brute-force attacks.

### 3. Authorization & Governance
* **RBAC (Role-Based Access Control):** Uses a hierarchical permission model defined in `roles.json`.
* **Role Inheritance:** Supports complex permission structures where administrative roles can inherit permissions from base roles.
* **Comprehensive Audit Logging:** Every login attempt, administrative change, and access denial is timestamped and recorded in `audit.log` for forensic analysis.

## 🛠️ Tech Stack
* **Language:** Python 3.x
* **Database:** SQLite3 (Stateful persistence)
* **Security Libraries:** Bcrypt (Hashing), Re (Regex validation)
* **Deployment:** Docker (Containerized environment)

## 📦 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/iam-lab-simulator.git](https://github.com/YOUR_USERNAME/iam-lab-simulator.git)
   cd iam-lab-simulator


## 👤 Author
**Eojin Kim** *Focus: Identity & Access Management (IAM) and Security Operations.*