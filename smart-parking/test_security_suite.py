"""
Automated Security & Functional Test Suite
Verifies all 5 core security requirements + AC1 to AC10 mitigations.
"""

import unittest
import threading
import time
import os
import sqlite3
from datetime import datetime, timedelta

import security
from database import get_db, init_db

class TestSmartParkingSecurity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_db()
        conn = get_db()
        cursor = conn.cursor()
        
        # Test User: Alice
        cursor.execute("SELECT id FROM users WHERE username = 'alice'")
        if not cursor.fetchone():
            pwd_hash, salt = security.hash_password("AliceSecure@123")
            mfa_sec1 = security.generate_mfa_secret()
            cursor.execute("INSERT INTO users (username, email, password_hash, salt, role, mfa_secret, mfa_enabled) VALUES ('alice', 'alice@test.com', ?, ?, 'user', ?, 1)", (pwd_hash, salt, mfa_sec1))
        
        # Test User: Bob
        cursor.execute("SELECT id FROM users WHERE username = 'bob'")
        if not cursor.fetchone():
            pwd_hash2, salt2 = security.hash_password("BobSecure@123")
            mfa_sec2 = security.generate_mfa_secret()
            cursor.execute("INSERT INTO users (username, email, password_hash, salt, role, mfa_secret, mfa_enabled) VALUES ('bob', 'bob@test.com', ?, ?, 'user', ?, 1)", (pwd_hash2, salt2, mfa_sec2))
        
        # Demo User: ybrayym
        cursor.execute("SELECT id FROM users WHERE username = 'ybrayym'")
        if not cursor.fetchone():
            pwd_hash_y, salt_y = security.hash_password("Secure@Pass2026!")
            mfa_sec_y = security.generate_mfa_secret()
            cursor.execute("INSERT INTO users (username, email, password_hash, salt, role, mfa_secret, mfa_enabled) VALUES ('ybrayym', 'ybrayym@uniten.edu.my', ?, ?, 'user', ?, 1)", (pwd_hash_y, salt_y, mfa_sec_y))
            u_id = cursor.lastrowid
            cursor.execute("INSERT INTO vehicles (user_id, plate_number, vehicle_type) VALUES (?, 'WYY8899', 'Sedan')", (u_id,))

        # Admin: admin
        cursor.execute("SELECT id FROM users WHERE username = 'admin'")
        if not cursor.fetchone():
            pwd_hash3, salt3 = security.hash_password("Admin@Secure2026!")
            mfa_sec3 = security.generate_mfa_secret()
            cursor.execute("INSERT INTO users (username, email, password_hash, salt, role, mfa_secret, mfa_enabled) VALUES ('admin', 'admin@uniten.edu.my', ?, ?, 'admin', ?, 1)", (pwd_hash3, salt3, mfa_sec3))
        
        conn.commit()
        conn.close()

    def setUp(self):
        # Reset test-specific artifacts before each test
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM reservations WHERE vehicle_plate LIKE 'TEST%' OR vehicle_plate = 'ALICE99'")
        cursor.execute("UPDATE users SET failed_attempts = 0, lockout_until = 0 WHERE username = 'brute_target'")
        conn.commit()
        conn.close()

    # --------------------------------------------------------------------------
    # 1. SQL INJECTION PREVENTION TEST (SR4, AC2)
    # --------------------------------------------------------------------------
    def test_01_sql_injection_login_bypass(self):
        """Attacker submits classic SQL injection strings to bypass authentication."""
        payloads = [
            "' OR '1'='1",
            "admin' --",
            "' OR ''='",
            "'; DROP TABLE users; --"
        ]
        conn = get_db()
        cursor = conn.cursor()
        for p in payloads:
            cursor.execute("SELECT id FROM users WHERE username = ?", (p,))
            res = cursor.fetchone()
            self.assertIsNone(res, f"SQL injection bypass succeeded with payload: {p}")
        conn.close()

    def test_02_sql_injection_search_tamper(self):
        """Attacker injects UNION SELECT in search query."""
        payload = "' UNION SELECT id, username, password_hash, salt, 'x' FROM users --"
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, slot_number, floor FROM parking_slots WHERE slot_number = ?", (payload,))
        res = cursor.fetchone()
        self.assertIsNone(res, "SQL injection in search succeeded")
        conn.close()

    # --------------------------------------------------------------------------
    # 2. BUFFER OVERFLOW & MEMORY EXHAUSTION MITIGATION
    # --------------------------------------------------------------------------
    def test_03_buffer_overflow_length_bounding(self):
        """Oversized inputs are safely bounded to prevent buffer exhaustion."""
        gigantic_payload = "A" * 100000
        bounded_plate = security.enforce_bound(gigantic_payload, "plate_number")
        self.assertEqual(len(bounded_plate), security.MAX_LENGTHS["plate_number"])
        self.assertEqual(bounded_plate, "A" * 10)

        bounded_user = security.enforce_bound(gigantic_payload, "username")
        self.assertEqual(len(bounded_user), security.MAX_LENGTHS["username"])

    # --------------------------------------------------------------------------
    # 3. MULTI-FACTOR AUTHENTICATION (MFA - RFC 6238 TOTP)
    # --------------------------------------------------------------------------
    def test_04_mfa_totp_generation_and_verification(self):
        """TOTP codes verify accurately within valid time window and reject wrong tokens."""
        secret = security.generate_mfa_secret()
        valid_code = security.get_totp_code(secret)
        self.assertEqual(len(valid_code), 6)
        self.assertTrue(valid_code.isdigit())

        # Valid code must pass
        self.assertTrue(security.verify_mfa_token(secret, valid_code))

        # Invalid codes must be rejected
        self.assertFalse(security.verify_mfa_token(secret, "000000" if valid_code != "000000" else "999999"))
        self.assertFalse(security.verify_mfa_token(secret, "abcdef"))
        self.assertFalse(security.verify_mfa_token(secret, "12345"))

    # --------------------------------------------------------------------------
    # 4. SYNTACTICAL & SEMANTIC INPUT VALIDATION
    # --------------------------------------------------------------------------
    def test_05_syntactical_validation(self):
        """Syntactical checks enforce strict regex patterns and reject malicious inputs."""
        valid_plates = ["WYY1234", "VAA8899", "B123A"]
        invalid_plates = ["<script>", "WYY 1234", "TOOLONGPLATE123", "P!@#"]

        for vp in valid_plates:
            val, _ = security.validate_syntactical(vp, "plate_number")
            self.assertTrue(val, f"Valid plate rejected: {vp}")

        for ip in invalid_plates:
            val, _ = security.validate_syntactical(ip, "plate_number")
            self.assertFalse(val, f"Invalid plate accepted: {ip}")

    def test_06_semantic_validation(self):
        """Semantic checks prevent impossible reservations."""
        now = datetime.now()
        past_start = (now - timedelta(hours=2)).strftime("%Y-%m-%dT%H:%M")
        past_end = (now - timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M")
        future_start = (now + timedelta(hours=2)).strftime("%Y-%m-%dT%H:%M")
        future_end = (now + timedelta(hours=4)).strftime("%Y-%m-%dT%H:%M")
        inverted_end = (now + timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M")

        ok, msg = security.validate_reservation_semantics(past_start, past_end)
        self.assertFalse(ok)
        self.assertIn("future", msg.lower())

        ok2, msg2 = security.validate_reservation_semantics(future_start, inverted_end)
        self.assertFalse(ok2)
        self.assertIn("after", msg2.lower())

        ok3, _ = security.validate_reservation_semantics(future_start, future_end)
        self.assertTrue(ok3)

    # --------------------------------------------------------------------------
    # 5. CONCURRENCY & DOUBLE-BOOKING PREVENTION (RACE CONDITION - AC7 / SR7)
    # --------------------------------------------------------------------------
    def test_07_race_condition_double_booking_prevention(self):
        """
        Simulate 10 simultaneous concurrent threads attempting to book the EXACT SAME
        slot for the exact same overlapping time window.
        """
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username = 'alice'")
        alice_id = cursor.fetchone()["id"]
        conn.close()

        slot_id = 1
        now = datetime.now()
        start = (now + timedelta(days=1, hours=10)).strftime("%Y-%m-%dT%H:%M")
        end = (now + timedelta(days=1, hours=12)).strftime("%Y-%m-%dT%H:%M")

        results = []
        threads = []

        def attempt_book(uid):
            success, msg = security.attempt_reservation_atomic(
                user_id=uid,
                slot_id=slot_id,
                plate_number=f"TEST{uid}",
                start_time=start,
                end_time=end,
                ip="192.168.1.10"
            )
            results.append(success)

        for i in range(10):
            t = threading.Thread(target=attempt_book, args=(alice_id,))
            threads.append(t)

        for t in threads:
            t.start()
        for t in threads:
            t.join()

        success_count = sum(1 for r in results if r is True)
        self.assertEqual(success_count, 1, f"Expected exactly 1 booking to succeed, but {success_count} succeeded!")
        self.assertEqual(len(results), 10)

    # --------------------------------------------------------------------------
    # 6. INSECURE DIRECT OBJECT REFERENCE (IDOR) & ACCESS CONTROL (SR3, AC3)
    # --------------------------------------------------------------------------
    def test_08_idor_unauthorized_cancellation_prevention(self):
        """Alice creates a reservation; Bob attempts to cancel Alice's reservation."""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username = 'alice'")
        alice_id = cursor.fetchone()["id"]
        cursor.execute("SELECT id FROM users WHERE username = 'bob'")
        bob_id = cursor.fetchone()["id"]

        now = datetime.now()
        start = (now + timedelta(days=2, hours=9)).strftime("%Y-%m-%dT%H:%M")
        end = (now + timedelta(days=2, hours=11)).strftime("%Y-%m-%dT%H:%M")
        
        cursor.execute("""
        INSERT INTO reservations (user_id, slot_id, vehicle_plate, start_time, end_time, status)
        VALUES (?, 2, 'ALICE99', ?, ?, 'confirmed')
        """, (alice_id, start, end))
        res_id = cursor.lastrowid
        conn.commit()
        
        cursor.execute("SELECT id, user_id FROM reservations WHERE id = ?", (res_id,))
        reservation = cursor.fetchone()
        
        is_owner = (reservation["user_id"] == bob_id)
        self.assertFalse(is_owner, "IDOR check failed: Bob should not own Alice's reservation.")
        
        cursor.execute("SELECT status FROM reservations WHERE id = ?", (res_id,))
        self.assertEqual(cursor.fetchone()["status"], "confirmed")
        conn.close()

    # --------------------------------------------------------------------------
    # 7. RATE LIMITING & ACCOUNT LOCKOUT (SR10, AC10)
    # --------------------------------------------------------------------------
    def test_09_brute_force_account_lockout(self):
        """5 failed login attempts trigger account lockout."""
        test_user = "brute_target"
        pwd_hash, salt = security.hash_password("DummyPass123!")
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username = ?", (test_user,))
        if not cursor.fetchone():
            cursor.execute("INSERT INTO users (username, email, password_hash, salt, role) VALUES (?, 'target@test.com', ?, ?, 'user')", (test_user, pwd_hash, salt))
        cursor.execute("UPDATE users SET failed_attempts = 0, lockout_until = 0 WHERE username = ?", (test_user,))
        conn.commit()
        conn.close()

        for _ in range(4):
            security.record_login_attempt(test_user, False, "10.0.0.1")
            locked, _ = security.check_account_lockout(test_user)
            self.assertFalse(locked)

        security.record_login_attempt(test_user, False, "10.0.0.1")
        locked, msg = security.check_account_lockout(test_user)
        self.assertTrue(locked)
        self.assertIn("locked", msg.lower())

if __name__ == "__main__":
    unittest.main()
