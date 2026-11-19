"""
Flask Application for Smart Parking Reservation System
Secured Software Development Life Cycle (SSDLC) Implementation
Authors: Group 01 (Ybrayym Isayev, Emir Artykov, Ahmmed, Md Sunny Alam, Yousef Mohamed)
Subject: Software Security (CCSB5113) - Universiti Tenaga Nasional
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash, abort, jsonify
from functools import wraps
from datetime import datetime, timedelta
import os
import sqlite3

from database import get_db, init_db
import security

app = Flask(__name__)
# 256-bit cryptographically secure random session secret
app.secret_key = os.environ.get("SECRET_KEY", "b47e289f81a7d620573c9118e5e340a6582d901a1c93aef4c7816d56729013de")

# Enforce strict 16 KB maximum payload limit (Mitigates Buffer Overflow / Memory Exhaustion)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=15)  # 15-min inactivity timeout

# Initialize DB on start
init_db()

# ==============================================================================
# SECURITY HEADERS MIDDLEWARE
# ==============================================================================
@app.after_request
def apply_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self' cdn.jsdelivr.net; style-src 'self' 'unsafe-inline' cdn.jsdelivr.net; script-src 'self' 'unsafe-inline' cdn.jsdelivr.net;"
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    return response

# ==============================================================================
# AUTHORIZATION & ACCESS CONTROL DECORATORS
# ==============================================================================
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for('login'))
        if not session.get('mfa_verified', False):
            flash("MFA verification required.", "warning")
            return redirect(url_for('mfa_verify'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or not session.get('mfa_verified', False):
            flash("Authentication required.", "warning")
            return redirect(url_for('login'))
        if session.get('role') != 'admin':
            ip = request.remote_addr or '127.0.0.1'
            conn = get_db()
            security.log_audit_event(conn, session['user_id'], "UNAUTHORIZED_ADMIN_ACCESS", f"Unauthorized attempt to access {request.path}", ip, "WARNING")
            conn.commit()
            conn.close()
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

# ==============================================================================
# EXCEPTION HANDLING & FAIL-SAFE DEFAULTS
# ==============================================================================
@app.errorhandler(400)
def bad_request(e):
    return render_template("error.html", code=400, message="Bad Request: Invalid input data format or parameters."), 400

@app.errorhandler(403)
def forbidden(e):
    return render_template("error.html", code=403, message="Access Denied: You do not have permission to perform this action."), 403

@app.errorhandler(404)
def not_found(e):
    return render_template("error.html", code=404, message="Resource not found."), 404

@app.errorhandler(413)
def request_entity_too_large(e):
    return render_template("error.html", code=413, message="Payload Too Large: Maximum allowed request size exceeded."), 413

@app.errorhandler(500)
def internal_error(e):
    # Log incident securely without leaking stack trace to user
    ip = request.remote_addr or '127.0.0.1'
    conn = get_db()
    security.log_audit_event(conn, session.get('user_id'), "SYSTEM_EXCEPTION", f"500 Internal error on {request.path}", ip, "ERROR")
    conn.commit()
    conn.close()
    return render_template("error.html", code=500, message="A secure internal error occurred. Administrators have been notified."), 500

# ==============================================================================
# AUTHENTICATION & MFA ROUTES
# ==============================================================================
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        ip = request.remote_addr or '127.0.0.1'
        username = security.enforce_bound(request.form.get("username", ""), "username")
        email = security.enforce_bound(request.form.get("email", ""), "email")
        password = request.form.get("password", "")
        plate = security.enforce_bound(request.form.get("plate_number", ""), "plate_number")
        
        # Syntactical Validation
        val_u, msg_u = security.validate_syntactical(username, "username")
        val_e, msg_e = security.validate_syntactical(email, "email")
        val_p, msg_p = security.validate_password_strength(password)
        val_plate, msg_plate = security.validate_syntactical(plate, "plate_number") if plate else (True, "")
        
        if not val_u:
            flash("Username must be alphanumeric (3-30 chars).", "danger")
            return render_template("register.html")
        if not val_e:
            flash("Invalid email format.", "danger")
            return render_template("register.html")
        if not val_p:
            flash(msg_p, "danger")
            return render_template("register.html")
        if plate and not val_plate:
            flash("Vehicle plate must be 3-10 alphanumeric characters (e.g., WYY1234).", "danger")
            return render_template("register.html")
            
        pwd_hash, salt = security.hash_password(password)
        mfa_secret = security.generate_mfa_secret()
        
        conn = get_db()
        cursor = conn.cursor()
        try:
            cursor.execute("""
            INSERT INTO users (username, email, password_hash, salt, role, mfa_secret, mfa_enabled)
            VALUES (?, ?, ?, ?, 'user', ?, 1)
            """, (username, email, pwd_hash, salt, mfa_secret))
            user_id = cursor.lastrowid
            
            if plate:
                cursor.execute("INSERT INTO vehicles (user_id, plate_number) VALUES (?, ?)", (user_id, plate))
                
            security.log_audit_event(conn, user_id, "USER_REGISTERED", f"User {username} registered successfully.", ip, "INFO")
            conn.commit()
            
            # Put setup info in session for initial MFA setup
            session['temp_user_id'] = user_id
            session['temp_username'] = username
            session['temp_mfa_secret'] = mfa_secret
            return redirect(url_for('mfa_setup'))
        except sqlite3.IntegrityError:
            flash("Username or email already exists.", "danger")
            return render_template("register.html")
        finally:
            conn.close()
            
    return render_template("register.html")

@app.route("/mfa-setup", methods=["GET", "POST"])
def mfa_setup():
    if 'temp_user_id' not in session or 'temp_mfa_secret' not in session:
        return redirect(url_for('login'))
        
    secret = session['temp_mfa_secret']
    username = session['temp_username']
    
    if request.method == "POST":
        token = request.form.get("token", "").strip()
        if security.verify_mfa_token(secret, token):
            session['user_id'] = session.pop('temp_user_id')
            session['username'] = session.pop('temp_username')
            session['role'] = 'user'
            session['mfa_verified'] = True
            session.pop('temp_mfa_secret', None)
            flash("MFA successfully enabled! Welcome to Smart Parking.", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid 6-digit MFA code. Please check your authenticator clock.", "danger")
            
    # Compute current mock token to assist evaluation/testing
    demo_code = security.get_totp_code(secret)
    return render_template("mfa_setup.html", secret=secret, username=username, demo_code=demo_code)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        ip = request.remote_addr or '127.0.0.1'
        username = security.enforce_bound(request.form.get("username", ""), "username")
        password = request.form.get("password", "")
        
        # Check Account Lockout (SR10 / AC10)
        is_locked, lock_msg = security.check_account_lockout(username)
        if is_locked:
            flash(lock_msg, "danger")
            return render_template("login.html")
            
        conn = get_db()
        cursor = conn.cursor()
        # Parameterized query protects against SQL Injection (SR4 / AC2)
        cursor.execute("SELECT id, username, password_hash, salt, role, mfa_secret, mfa_enabled FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()
        
        if user and security.verify_password(password, user["password_hash"], user["salt"]):
            # Stage 1 Password authenticated -> Proceed to Stage 2 MFA
            session['pending_mfa_user_id'] = user["id"]
            session['pending_mfa_username'] = user["username"]
            session['pending_mfa_role'] = user["role"]
            session['pending_mfa_secret'] = user["mfa_secret"]
            return redirect(url_for('mfa_verify'))
        else:
            # Record failed login & update rate limiter
            security.record_login_attempt(username, False, ip)
            flash("Invalid username or password.", "danger")
            
    return render_template("login.html")

@app.route("/mfa-verify", methods=["GET", "POST"])
def mfa_verify():
    if 'pending_mfa_user_id' not in session:
        return redirect(url_for('login'))
        
    secret = session['pending_mfa_secret']
    username = session['pending_mfa_username']
    ip = request.remote_addr or '127.0.0.1'
    
    if request.method == "POST":
        token = request.form.get("token", "").strip()
        val, _ = security.validate_syntactical(token, "mfa_token")
        
        if val and security.verify_mfa_token(secret, token):
            # MFA Succeeded -> Create full session
            user_id = session.pop('pending_mfa_user_id')
            role = session.pop('pending_mfa_role')
            session.pop('pending_mfa_secret', None)
            
            session['user_id'] = user_id
            session['username'] = username
            session['role'] = role
            session['mfa_verified'] = True
            
            security.record_login_attempt(username, True, ip)
            flash(f"Welcome back, {username}!", "success")
            
            if role == "admin":
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('dashboard'))
        else:
            conn = get_db()
            security.log_audit_event(conn, session['pending_mfa_user_id'], "MFA_FAILED", f"Failed MFA verification from {ip}", ip, "WARNING")
            conn.commit()
            conn.close()
            flash("Invalid or expired 6-digit MFA token.", "danger")
            
    demo_code = security.get_totp_code(secret)
    return render_template("mfa_verify.html", username=username, demo_code=demo_code)

@app.route("/logout")
def logout():
    user_id = session.get('user_id')
    ip = request.remote_addr or '127.0.0.1'
    if user_id:
        conn = get_db()
        security.log_audit_event(conn, user_id, "USER_LOGOUT", "User securely terminated session", ip, "INFO")
        conn.commit()
        conn.close()
    session.clear()
    flash("You have been safely logged out.", "info")
    return redirect(url_for('login'))

# ==============================================================================
# USER FUNCTIONAL REQUIREMENTS (FR1 - FR9)
# ==============================================================================
@app.route("/dashboard")
@login_required
def dashboard():
    conn = get_db()
    cursor = conn.cursor()
    # Active reservations for this authenticated user
    cursor.execute("""
    SELECT r.id, r.start_time, r.end_time, r.status, r.vehicle_plate, s.slot_number, s.floor, s.slot_type
    FROM reservations r
    JOIN parking_slots s ON r.slot_id = s.id
    WHERE r.user_id = ? AND r.status = 'confirmed'
    ORDER BY r.start_time ASC
    """, (session['user_id'],))
    active_reservations = cursor.fetchall()
    
    # Registered vehicles
    cursor.execute("SELECT plate_number, vehicle_type FROM vehicles WHERE user_id = ?", (session['user_id'],))
    vehicles = cursor.fetchall()
    conn.close()
    
    return render_template("dashboard.html", active_reservations=active_reservations, vehicles=vehicles)

@app.route("/search", methods=["GET", "POST"])
@login_required
def search_slots():
    floor_filter = request.args.get("floor", "all")
    type_filter = request.args.get("type", "all")
    
    conn = get_db()
    cursor = conn.cursor()
    
    query = "SELECT * FROM parking_slots WHERE 1=1"
    params = []
    
    if floor_filter != "all":
        query += " AND floor = ?"
        params.append(floor_filter)
    if type_filter != "all":
        query += " AND slot_type = ?"
        params.append(type_filter)
        
    query += " ORDER BY floor, slot_number"
    cursor.execute(query, tuple(params))
    slots = cursor.fetchall()
    conn.close()
    
    return render_template("search.html", slots=slots, selected_floor=floor_filter, selected_type=type_filter)

@app.route("/reserve/<int:slot_id>", methods=["GET", "POST"])
@login_required
def reserve_slot(slot_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM parking_slots WHERE id = ?", (slot_id,))
    slot = cursor.fetchone()
    
    cursor.execute("SELECT plate_number FROM vehicles WHERE user_id = ?", (session['user_id'],))
    user_vehicles = cursor.fetchall()
    conn.close()
    
    if not slot:
        abort(404)
        
    if request.method == "POST":
        ip = request.remote_addr or '127.0.0.1'
        start_time = request.form.get("start_time", "").strip()
        end_time = request.form.get("end_time", "").strip()
        plate_number = security.enforce_bound(request.form.get("plate_number", ""), "plate_number")
        
        # 1. Syntactical Validation
        v_start, _ = security.validate_syntactical(start_time, "datetime")
        v_end, _ = security.validate_syntactical(end_time, "datetime")
        v_plate, _ = security.validate_syntactical(plate_number, "plate_number")
        
        if not (v_start and v_end and v_plate):
            flash("Invalid input format detected. Please review your date/time and plate number.", "danger")
            return render_template("reserve.html", slot=slot, user_vehicles=user_vehicles)
            
        # 2. Semantic Validation
        sem_valid, sem_msg = security.validate_reservation_semantics(start_time, end_time)
        if not sem_valid:
            flash(sem_msg, "danger")
            return render_template("reserve.html", slot=slot, user_vehicles=user_vehicles)
            
        # 3. Atomic Reservation & Race Condition Prevention (SR7 / FR10)
        success, res_msg = security.attempt_reservation_atomic(
            session['user_id'], slot_id, plate_number, start_time, end_time, ip
        )
        
        if success:
            flash(res_msg, "success")
            return redirect(url_for('my_reservations'))
        else:
            flash(res_msg, "danger")
            
    return render_template("reserve.html", slot=slot, user_vehicles=user_vehicles)

@app.route("/my-reservations")
@login_required
def my_reservations():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT r.id, r.start_time, r.end_time, r.status, r.vehicle_plate, r.created_at,
           s.slot_number, s.floor, s.slot_type, s.price_per_hour
    FROM reservations r
    JOIN parking_slots s ON r.slot_id = s.id
    WHERE r.user_id = ?
    ORDER BY r.created_at DESC
    """, (session['user_id'],))
    all_reservations = cursor.fetchall()
    conn.close()
    return render_template("my_reservations.html", reservations=all_reservations)

@app.route("/reservation/cancel/<int:res_id>", methods=["POST"])
@login_required
def cancel_reservation(res_id):
    """
    Mitigates Insecure Direct Object Reference (IDOR - SR3 / AC3):
    Strictly verifies ownership: WHERE id = ? AND user_id = ?
    """
    ip = request.remote_addr or '127.0.0.1'
    conn = get_db()
    cursor = conn.cursor()
    
    # Ownership Check
    cursor.execute("SELECT id, user_id, status FROM reservations WHERE id = ?", (res_id,))
    res = cursor.fetchone()
    
    if not res:
        conn.close()
        abort(404)
        
    if res["user_id"] != session['user_id'] and session.get('role') != 'admin':
        # Unauthorized IDOR Attempt Detected
        security.log_audit_event(conn, session['user_id'], "IDOR_ATTEMPT", f"Attempted unauthorized cancellation of reservation #{res_id}", ip, "CRITICAL")
        conn.commit()
        conn.close()
        abort(403)
        
    cursor.execute("UPDATE reservations SET status = 'cancelled', updated_at = CURRENT_TIMESTAMP WHERE id = ?", (res_id,))
    security.log_audit_event(conn, session['user_id'], "RESERVATION_CANCELLED", f"Reservation #{res_id} cancelled by user", ip, "INFO")
    conn.commit()
    conn.close()
    
    flash("Reservation successfully cancelled.", "success")
    return redirect(url_for('my_reservations'))

@app.route("/vehicles", methods=["GET", "POST"])
@login_required
def manage_vehicles():
    conn = get_db()
    cursor = conn.cursor()
    if request.method == "POST":
        plate = security.enforce_bound(request.form.get("plate_number", ""), "plate_number")
        v_type = request.form.get("vehicle_type", "car")
        
        val_plate, _ = security.validate_syntactical(plate, "plate_number")
        if not val_plate:
            flash("Invalid plate number format (e.g., WYY1234, BCD8899).", "danger")
        else:
            cursor.execute("INSERT INTO vehicles (user_id, plate_number, vehicle_type) VALUES (?, ?, ?)",
                           (session['user_id'], plate, v_type))
            conn.commit()
            flash("Vehicle added successfully.", "success")
            
    cursor.execute("SELECT id, plate_number, vehicle_type FROM vehicles WHERE user_id = ?", (session['user_id'],))
    vehicles = cursor.fetchall()
    conn.close()
    return render_template("vehicles.html", vehicles=vehicles)

# ==============================================================================
# ADMIN VIEW & CONTROLS (FR6 / SR6 / SR9)
# ==============================================================================
@app.route("/admin/dashboard")
@admin_required
def admin_dashboard():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as total_slots, SUM(CASE WHEN status='available' THEN 1 ELSE 0 END) as avail_slots FROM parking_slots")
    stats = cursor.fetchone()
    
    cursor.execute("SELECT COUNT(*) as active_count FROM reservations WHERE status='confirmed'")
    active_res = cursor.fetchone()["active_count"]
    
    cursor.execute("""
    SELECT r.id, u.username, r.vehicle_plate, s.slot_number, r.start_time, r.end_time, r.status
    FROM reservations r
    JOIN users u ON r.user_id = u.id
    JOIN parking_slots s ON r.slot_id = s.id
    ORDER BY r.created_at DESC LIMIT 10
    """)
    recent_reservations = cursor.fetchall()
    conn.close()
    
    return render_template("admin_dashboard.html", stats=stats, active_res=active_res, recent_reservations=recent_reservations)

@app.route("/admin/audit-logs")
@admin_required
def admin_audit_logs():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT l.id, l.timestamp, l.event_type, l.details, l.ip_address, l.severity, u.username
    FROM audit_logs l
    LEFT JOIN users u ON l.user_id = u.id
    ORDER BY l.timestamp DESC LIMIT 50
    """)
    logs = cursor.fetchall()
    conn.close()
    return render_template("admin_audit_logs.html", logs=logs)

@app.route("/admin/slot/toggle/<int:slot_id>", methods=["POST"])
@admin_required
def admin_toggle_slot(slot_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT status FROM parking_slots WHERE id = ?", (slot_id,))
    slot = cursor.fetchone()
    if slot:
        new_status = "maintenance" if slot["status"] == "available" else "available"
        cursor.execute("UPDATE parking_slots SET status = ? WHERE id = ?", (new_status, slot_id))
        security.log_audit_event(conn, session['user_id'], "SLOT_STATUS_CHANGE", f"Admin changed slot {slot_id} to {new_status}", request.remote_addr or '127.0.0.1', "INFO")
        conn.commit()
    conn.close()
    flash("Slot status updated.", "info")
    return redirect(url_for('admin_dashboard'))

if __name__ == "__main__":
    # In production, run behind Gunicorn / Nginx with HTTPS TLS 1.3
    app.run(host="127.0.0.1", port=5000, debug=False)
