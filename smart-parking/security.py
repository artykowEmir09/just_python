"""
Security Module for Smart Parking Reservation System
Software Security (CCSB5113) - Assignment 2
Universiti Tenaga Nasional (UNITEN)

Core Security Mechanisms:
1. Multi-Factor Authentication (MFA - RFC 6238 TOTP)
2. Input Validation (Syntactical Regex & Semantic Rules)
3. SQL Injection Prevention (Strict Parameterized Queries)
4. Buffer Overflow & Memory Exhaustion Controls (Length Bounding & Payload Limits)
5. Structured Exception Handling & Fail-Safe Defaults
6. Password Security (PBKDF2-HMAC-SHA256 with Salt, 600k iterations)
7. Concurrency / Race Condition Prevention (ACID BEGIN IMMEDIATE)
8. Role-Based Access Control & Anti-IDOR Object Ownership
9. Rate Limiting & Account Lockout
10. Tamper-Resistant Security Audit Trail
"""

import os
import re
import time
import hmac
import hashlib
import struct
import base64
import secrets
from datetime import datetime
from database import get_db

# ==============================================================================
# 1. BUFFER OVERFLOW & MEMORY EXHAUSTION MITIGATION (Input Bounds)
# ==============================================================================
MAX_LENGTHS = {
    "username": 30,
    "email": 100,
    "password": 64,
    "plate_number": 10,
    "slot_number": 10,
    "search_query": 50,
    "mfa_token": 6,
    "general_text": 150
}

def enforce_bound(value: str, field_type: str) -> str:
    """
    Safely bounds input strings to prevent memory exhaustion,
    denial-of-service payloads, and C-runtime buffer overflows.
    """
    if not isinstance(value, str):
        return ""
    max_len = MAX_LENGTHS.get(field_type, 100)
    # Strip null bytes to prevent C-string termination truncation bugs
    sanitized = value.replace('\x00', '').strip()
    return sanitized[:max_len]

# ==============================================================================
# 2. SYNTACTICAL & SEMANTIC INPUT VALIDATION
# ==============================================================================
PATTERNS = {
    "username": r'^[a-zA-Z0-9_-]{3,30}$',
    "email": r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
    "plate_number": r'^[A-Z0-9]{3,10}$',  # Malaysian & International standard formats
    "mfa_token": r'^[0-9]{6}$',
    "datetime": r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}$'
}

def validate_password_strength(password: str) -> tuple[bool, str]:
    """Enforces enterprise password complexity requirements."""
    if len(password) < 10:
        return False, "Password must be at least 10 characters long."
    if len(password) > MAX_LENGTHS["password"]:
        return False, "Password exceeds maximum length (64 characters)."
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter."
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter."
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one numeric digit."
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character."
    return True, "Password meets complexity criteria."

def validate_syntactical(value: str, field_type: str) -> tuple[bool, str]:
    """
    Validates structural format against strict whitelists.
    Rejects strings exceeding max bounds without silent truncation.
    """
    if not isinstance(value, str):
        return False, "Input must be a valid string."
    
    max_len = MAX_LENGTHS.get(field_type, 100)
    if len(value) > max_len:
        return False, f"Input exceeds maximum allowed length of {max_len} characters."
        
    if field_type not in PATTERNS:
        return False, f"Unknown field type: {field_type}"
        
    sanitized = value.replace('\x00', '').strip()
    if not re.match(PATTERNS[field_type], sanitized):
        return False, f"Invalid format for {field_type}."
    return True, sanitized

def validate_reservation_semantics(start_time_str: str, end_time_str: str) -> tuple[bool, str]:
    """
    Semantic Validation:
    - Reservation start time must be in the future.
    - End time must be strictly after start time.
    - Booking duration bounded between 30 minutes and 24 hours.
    """
    try:
        start_dt = datetime.strptime(start_time_str, "%Y-%m-%dT%H:%M")
        end_dt = datetime.strptime(end_time_str, "%Y-%m-%dT%H:%M")
        now = datetime.now()
        
        if start_dt < now:
            return False, "Reservation start time must be in the future."
        if end_dt <= start_dt:
            return False, "End time must be strictly after start time."
            
        duration_hours = (end_dt - start_dt).total_seconds() / 3600.0
        if duration_hours > 24.0:
            return False, "Maximum reservation duration is 24 hours."
        if duration_hours < 0.5:
            return False, "Minimum reservation duration is 30 minutes."
            
        return True, "Semantic validation passed."
    except ValueError:
        return False, "Malformed datetime format. Expected YYYY-MM-DDTHH:MM."

# ==============================================================================
# 3. MULTI-FACTOR AUTHENTICATION (MFA - RFC 6238 TOTP)
# ==============================================================================
def generate_mfa_secret() -> str:
    """Generates a cryptographically secure 160-bit Base32 secret for TOTP."""
    random_bytes = secrets.token_bytes(20)
    return base64.b32encode(random_bytes).decode('utf-8')

def get_totp_code(secret_b32: str, timestamp: float = None, time_step: int = 30, digits: int = 6) -> str:
    """Generates TOTP code using HMAC-SHA1 according to RFC 6238."""
    if timestamp is None:
        timestamp = time.time()
    try:
        key = base64.b32decode(secret_b32, casefold=True)
    except Exception:
        return ""
    counter = int(timestamp // time_step)
    msg = struct.pack(">Q", counter)
    h = hmac.new(key, msg, hashlib.sha1).digest()
    o = h[19] & 0x0F
    code = (struct.unpack(">I", h[o:o+4])[0] & 0x7FFFFFFF) % (10 ** digits)
    return f"{code:0{digits}d}"

def verify_mfa_token(secret_b32: str, token: str, window: int = 1) -> bool:
    """Verifies MFA token with clock drift tolerance (±1 step / 30 seconds)."""
    if not token or len(token) != 6 or not token.isdigit():
        return False
    now = time.time()
    for w in range(-window, window + 1):
        if get_totp_code(secret_b32, timestamp=now + (w * 30)) == token:
            return True
    return False

# ==============================================================================
# 4. PASSWORD SECURITY (PBKDF2-HMAC-SHA256)
# ==============================================================================
def hash_password(password: str) -> tuple[str, str]:
    """Generates salt and PBKDF2-HMAC-SHA256 hash (600,000 iterations)."""
    salt = secrets.token_hex(16)
    pwd_hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        600000
    ).hex()
    return pwd_hash, salt

def verify_password(password: str, stored_hash: str, salt: str) -> bool:
    """Verifies password using constant-time comparison to prevent timing attacks."""
    computed_hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        600000
    ).hex()
    return hmac.compare_digest(computed_hash, stored_hash)

# ==============================================================================
# 5. RATE LIMITING & BRUTE FORCE LOCKOUT (SR10 / AC10)
# ==============================================================================
MAX_FAILED_ATTEMPTS = 5
LOCKOUT_DURATION = 900  # 15 minutes in seconds

def check_account_lockout(username: str) -> tuple[bool, str]:
    """Checks if an account is currently locked out."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT failed_attempts, lockout_until FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return False, ""
    
    failed_attempts, lockout_until = row["failed_attempts"], row["lockout_until"]
    now = time.time()
    if lockout_until > now:
        remaining = int((lockout_until - now) / 60) + 1
        return True, f"Account locked due to multiple failed attempts. Try again in {remaining} minute(s)."
    return False, ""

def record_login_attempt(username: str, success: bool, ip: str):
    """Updates failed attempt counter and sets lockout timestamp if threshold exceeded."""
    conn = get_db()
    cursor = conn.cursor()
    now = time.time()
    if success:
        cursor.execute("UPDATE users SET failed_attempts = 0, lockout_until = 0 WHERE username = ?", (username,))
        log_audit_event(conn, username, "LOGIN_SUCCESS", f"User logged in from {ip}", ip, "INFO")
    else:
        cursor.execute("SELECT failed_attempts FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        if row:
            attempts = row["failed_attempts"] + 1
            if attempts >= MAX_FAILED_ATTEMPTS:
                lockout = now + LOCKOUT_DURATION
                cursor.execute("UPDATE users SET failed_attempts = ?, lockout_until = ? WHERE username = ?", (attempts, lockout, username))
                log_audit_event(conn, username, "ACCOUNT_LOCKED", f"Account locked after {attempts} failed attempts from {ip}", ip, "WARNING")
            else:
                cursor.execute("UPDATE users SET failed_attempts = ? WHERE username = ?", (attempts, username))
                log_audit_event(conn, username, "LOGIN_FAILED", f"Failed login attempt ({attempts}/{MAX_FAILED_ATTEMPTS}) from {ip}", ip, "WARNING")
    conn.commit()
    conn.close()

# ==============================================================================
# 6. SECURITY AUDIT LOGGING (SR9 / AC9)
# ==============================================================================
def log_audit_event(conn, user_identifier, event_type: str, details: str, ip: str, severity: str = "INFO"):
    """Inserts structured audit trail record into tamper-resistant audit log table."""
    try:
        user_id = None
        if isinstance(user_identifier, int):
            user_id = user_identifier
        elif isinstance(user_identifier, str):
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE username = ?", (user_identifier,))
            u = cursor.fetchone()
            if u:
                user_id = u["id"]
                
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO audit_logs (user_id, event_type, details, ip_address, severity)
        VALUES (?, ?, ?, ?, ?)
        """, (user_id, event_type, details[:250], ip[:45], severity))
    except Exception as e:
        print(f"[AUDIT LOG ERROR] Failed to record event: {e}")

# ==============================================================================
# 7. CONCURRENCY & DOUBLE-BOOKING PREVENTION (SR7 / FR10 / AC7)
# ==============================================================================
def attempt_reservation_atomic(user_id: int, slot_id: int, plate_number: str, start_time: str, end_time: str, ip: str) -> tuple[bool, str]:
    """
    Mitigates AC7 / SR7 Race Conditions:
    Uses SQLite immediate write transaction lock to eliminate TOCTOU window.
    """
    conn = get_db()
    try:
        cursor = conn.cursor()
        # Acquire transaction write lock immediately
        cursor.execute("BEGIN IMMEDIATE")
        
        # Check slot exists and is active
        cursor.execute("SELECT id, slot_number, status FROM parking_slots WHERE id = ?", (slot_id,))
        slot = cursor.fetchone()
        if not slot:
            conn.rollback()
            return False, "Parking slot does not exist."
        if slot["status"] != "available":
            conn.rollback()
            return False, f"Parking slot {slot['slot_number']} is currently unavailable ({slot['status']})."
            
        # Check for overlapping active reservations on the exact same slot
        cursor.execute("""
        SELECT id FROM reservations
        WHERE slot_id = ?
          AND status = 'confirmed'
          AND (start_time < ? AND end_time > ?)
        """, (slot_id, end_time, start_time))
        conflict = cursor.fetchone()
        
        if conflict:
            conn.rollback()
            log_audit_event(conn, user_id, "BOOKING_CONFLICT", f"Double-booking prevented on slot {slot_id}", ip, "WARNING")
            conn.commit()
            return False, "Slot has already been reserved for the requested time period by another user."
            
        # Insert confirmed reservation
        cursor.execute("""
        INSERT INTO reservations (user_id, slot_id, vehicle_plate, start_time, end_time, status)
        VALUES (?, ?, ?, ?, ?, 'confirmed')
        """, (user_id, slot_id, plate_number, start_time, end_time))
        
        res_id = cursor.lastrowid
        log_audit_event(conn, user_id, "RESERVATION_CREATED", f"Reservation #{res_id} created for slot {slot['slot_number']} ({plate_number})", ip, "INFO")
        
        conn.commit()
        return True, f"Reservation successfully confirmed! Reference ID: #{res_id}"
    except Exception as e:
        conn.rollback()
        return False, "A secure system error occurred while processing reservation. Please try again."
    finally:
        conn.close()
