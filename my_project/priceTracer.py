"""Price tracker: scrapes product prices, stores history in SQLite,
and emails you when a price drops to/below your target or falls since last check.

Usage:
    python price_tracker.py            # check once
    python price_tracker.py --dry-run  # print alerts instead of emailing
    python price_tracker.py --loop 60  # check every 60 minutes
    python price_tracker.py --history  # show stored price history
"""
import argparse, json, os, re, smtplib, sqlite3, time
from datetime import datetime
from email.message import EmailMessage

import requests
from bs4 import BeautifulSoup

DB_FILE = "prices.db"
CONFIG_FILE = "products.json"
HEADERS = {"User-Agent": "Mozilla/5.0 (personal price tracker; contact: you@example.com)"}


def init_db():
    con = sqlite3.connect(DB_FILE)
    con.execute("""CREATE TABLE IF NOT EXISTS prices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT, url TEXT, price REAL, checked_at TEXT)""")
    return con


def parse_price(text):
    """Turn 'RM 1,299.90' or '$1.299,90' style text into a float."""
    cleaned = re.sub(r"[^\d.,]", "", text)
    if not cleaned:
        raise ValueError(f"No digits in price text: {text!r}")
    # If both separators exist, the last one is the decimal separator.
    if "," in cleaned and "." in cleaned:
        if cleaned.rfind(",") > cleaned.rfind("."):
            cleaned = cleaned.replace(".", "").replace(",", ".")
        else:
            cleaned = cleaned.replace(",", "")
    elif "," in cleaned:
        # '1,299' -> thousands; '12,50' -> decimal
        cleaned = cleaned.replace(",", "") if re.search(r",\d{3}$", cleaned) else cleaned.replace(",", ".")
    return float(cleaned)


def fetch_price(url, selector):
    resp = requests.get(url, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    el = soup.select_one(selector)
    if el is None:
        raise ValueError(f"CSS selector {selector!r} matched nothing (page layout changed?)")
    return parse_price(el.get_text(strip=True))


def last_price(con, url):
    row = con.execute("SELECT price FROM prices WHERE url=? ORDER BY id DESC LIMIT 1", (url,)).fetchone()
    return row[0] if row else None


def send_email(subject, body, dry_run):
    if dry_run:
        print(f"\n--- [DRY RUN] EMAIL ---\nSubject: {subject}\n{body}\n-----------------------")
        return
    # Credentials come from environment variables, never from the code.
    user, pw = os.environ["SMTP_USER"], os.environ["SMTP_PASS"]
    to = os.environ.get("ALERT_TO", user)
    host = os.environ.get("SMTP_HOST", "smtp.gmail.com")
    port = int(os.environ.get("SMTP_PORT", "465"))
    msg = EmailMessage()
    msg["Subject"], msg["From"], msg["To"] = subject, user, to
    msg.set_content(body)
    with smtplib.SMTP_SSL(host, port) as s:
        s.login(user, pw)
        s.send_message(msg)


def check_all(dry_run=False):
    with open(CONFIG_FILE) as f:
        products = json.load(f)
    con = init_db()
    for p in products:
        name, url = p["name"], p["url"]
        try:
            price = fetch_price(url, p["selector"])
        except Exception as e:
            print(f"[!] {name}: {e}")
            continue
        prev = last_price(con, url)
        con.execute("INSERT INTO prices (name,url,price,checked_at) VALUES (?,?,?,?)",
                    (name, url, price, datetime.now().isoformat(timespec="seconds")))
        con.commit()
        print(f"[+] {name}: {price:.2f}" + (f" (was {prev:.2f})" if prev is not None else " (first check)"))

        target = p.get("target_price")
        hit_target = target is not None and price <= target
        dropped = prev is not None and price < prev
        if hit_target or dropped:
            reason = f"reached your target of {target:.2f}" if hit_target else f"dropped from {prev:.2f}"
            send_email(f"Price drop: {name} now {price:.2f}",
                       f"{name} {reason}.\nCurrent price: {price:.2f}\n{url}", dry_run)
    con.close()


def show_history():
    con = init_db()
    for name, price, ts in con.execute("SELECT name, price, checked_at FROM prices ORDER BY name, id"):
        print(f"{ts}  {name:30s} {price:10.2f}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--loop", type=int, metavar="MINUTES")
    ap.add_argument("--history", action="store_true")
    a = ap.parse_args()
    if a.history:
        show_history()
    elif a.loop:
        while True:
            check_all(a.dry_run)
            time.sleep(a.loop * 60)
    else:
        check_all(a.dry_run)