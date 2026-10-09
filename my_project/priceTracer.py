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