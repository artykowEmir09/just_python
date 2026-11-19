# Smart Parking Reservation System (SSDLC Secured Prototype)
**Course:** CCSB5113 Software Security  
**Institution:** Universiti Tenaga Nasional (UNITEN), Putrajaya Campus  
**Scenario:** Scenario 1 – Smart Parking Reservation System  
**Class Group:** Group 01 (01B)  
**Authors:**
- Ybrayym Isayev (CS01084243) - Lead Security Architect, Input Validation & Buffer Controls
- Artykov Emir (bsw01085215) - Backend API, Database Concurrency & SQL Injection Defense
- Ahmmed (CS01084173) - Multi-Factor Authentication (MFA / TOTP) & Session Management
- Alam Md Sunny (BSW01085650) - Exception Handling, Audit Logging & Rate Limiting
- Yousef Mohamed Attia (SW01084180) - Threat Modeling (DFD), Access Control & UI Design

---

## 1. System Overview
The Smart Parking Reservation System is a production-ready, security-hardened web prototype developed adhering to the Secure Software Development Life Cycle (SSDLC). It implements all 10 Functional Requirements (FR1–FR10) and mitigates all 10 Abuse Cases (AC1–AC10) and Security Requirements (SR1–SR10) defined in Assignment 1.

---

## 2. Core Implemented Security Mechanisms
1. **Multi-Factor Authentication (MFA):** Native RFC 6238 Time-Based One-Time Password (TOTP) engine with 160-bit cryptographically secure Base32 secret keys and $\pm 1$ step clock drift window.
2. **Syntactical & Semantic Input Validation:**
   - Syntactical: Strict regex pattern whitelisting on vehicle plate numbers (`^[A-Z0-9]{3,10}$`), usernames, emails, and datetime strings.
   - Semantic: Chronological validation ensuring reservation start times are in the future, end times occur strictly after start times, and duration is bounded (30 mins to 24 hrs).
3. **SQL Injection Defense:** 100% prepared statements with parameterized inputs across all database interactions.
4. **Buffer Overflow & Memory Exhaustion Controls:** Strict 16 KB request body limit (`MAX_CONTENT_LENGTH = 16 * 1024`), null-byte stripping, and field-level character truncation bounds.
5. **Concurrency & Race Condition Prevention (Double-Booking Elimination):** Immediate write-lock (`BEGIN IMMEDIATE`) transaction isolation preventing Time-of-Check to Time-of-Use (TOCTOU) booking collisions.
6. **Access Control & Anti-IDOR:** Server-side object ownership verification (`WHERE id = ? AND user_id = ?`) preventing Insecure Direct Object References.
7. **Brute-Force Rate Limiting & Account Lockout:** Automatic 15-minute account lockout after 5 consecutive failed authentication attempts.
8. **Structured Exception Handling & Fail-Safe Defaults:** Intercepts 400, 403, 404, 413, and 500 errors to serve sanitized user messages while preventing stack trace / system disclosure.
9. **Tamper-Resistant Security Audit Logging:** Live append-only audit trail logging security events, severity levels, user identifiers, and IP addresses.

---

## 3. Quick Start & Execution Guide

### Prerequisites
- Python 3.10 or higher
- `pip` (Python package installer)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Initialize Database
```bash
python database.py
```
This initializes the SQLite schema (`smart_parking.db`) and pre-populates default parking slots across Ground, Level 1, and Level 2 floors.

### Step 3: Run Automated Security Test Suite
```bash
python -m unittest test_security_suite.py
```
Expected output:
```text
Ran 9 tests in ~1.9s
OK
```

### Step 4: Launch Web Application
```bash
python app.py
```
Open your browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 4. Default Testing Accounts
| Role | Username | Password | Notes |
| :--- | :--- | :--- | :--- |
| **Administrator** | `admin` | `Admin@Secure2026!` | Access to Admin Control Center, Bay Maintenance, & Security Audit Logs |
| **Standard User** | `ybrayym` | `Secure@Pass2026!` | Standard reservation, vehicle management, and slot booking |

*Note: For testing convenience during grading, the current valid 6-digit TOTP code is displayed dynamically on the MFA prompt screen.*

---

## 5. Project Directory Structure
```text
SmartParking_SecureSystem/
├── app.py                     # Main Flask web controller and security routing
├── database.py                # Database connection, schemas, and seeding
├── security.py                # TOTP engine, regex validators, bounds, & audit loggers
├── test_security_suite.py     # Automated security test suite (9 test cases)
├── requirements.txt           # Python dependency specification
├── README.md                  # Comprehensive setup and security documentation
├── templates/                 # Jinja2 HTML5 front-end templates
│   ├── base.html              # Responsive layout with security headers
│   ├── index.html             # Landing page with security control badges
│   ├── login.html             # Multi-stage user login view
│   ├── mfa_verify.html        # TOTP 6-digit verification interface
│   ├── mfa_setup.html         # Base32 TOTP QR/secret enrollment view
│   ├── register.html          # Registration with password complexity meter
│   ├── dashboard.html         # User dashboard displaying active reservations
│   ├── search.html            # Parameterized parking slot search & filters
│   ├── reserve.html           # Booking form with semantic date validation
│   ├── my_reservations.html   # Booking history and anti-IDOR cancellation
│   ├── vehicles.html          # Vehicle management view
│   ├── admin_dashboard.html   # Facility occupancy and slot maintenance panel
│   ├── admin_audit_logs.html  # Live security audit trail viewer
│   └── error.html             # Sanitized fail-safe error templates (400/403/404/500)
└── static/                    # Static assets
```
