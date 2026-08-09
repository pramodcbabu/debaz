"""Database Setup & Schema Definition for Nethra Intelligence Suite.

Database: nethra_campaign.db (SQLite)

Tables:
- constituencies: 234 Assembly Seats (ECI 2026 actuals, geo-fenced issues)
- parliaments: 39 Lok Sabha Seats (projected 2029, regional issues)
- gcc_wards: 200 Greater Chennai Corporation Wards (Zone-specific civic issues)
- issue_events: 6-month social & news events (Feb-Aug 2026) with spam score & geo-verification
- spam_filter_logs: Spam filtering audit log (detecting bot farms & duplicate spam)
"""

import sqlite3
import os

DB_PATH = "data/nethra_campaign.db"

def init_db():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Assembly Seats Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS constituencies (
        unit_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        region TEXT NOT NULL,
        district TEXT NOT NULL,
        lat REAL NOT NULL,
        lon REAL NOT NULL,
        voters INTEGER NOT NULL,
        winner_2026 TEXT NOT NULL,
        tvk_share_2026 REAL NOT NULL,
        dmk_share_2026 REAL NOT NULL,
        aiadmk_share_2026 REAL NOT NULL,
        margin_2026 INTEGER NOT NULL,
        tvk_fav REAL NOT NULL,
        dmk_fav REAL NOT NULL,
        aiadmk_fav REAL NOT NULL,
        bjp_fav REAL NOT NULL,
        tvk_lead REAL NOT NULL,
        status TEXT NOT NULL,
        top_issue TEXT NOT NULL,
        voter_salience INTEGER NOT NULL,
        tvk_messaging INTEGER NOT NULL,
        gap INTEGER NOT NULL,
        confidence INTEGER NOT NULL,
        source_name TEXT NOT NULL,
        source_url TEXT NOT NULL,
        methodology TEXT NOT NULL,
        whatsapp TEXT NOT NULL,
        instagram TEXT NOT NULL,
        twitter TEXT NOT NULL
    )
    """)

    # 2. Parliamentary Seats Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS parliaments (
        unit_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        region TEXT NOT NULL,
        lat REAL NOT NULL,
        lon REAL NOT NULL,
        voters INTEGER NOT NULL,
        tvk_proj REAL NOT NULL,
        dmk_proj REAL NOT NULL,
        aiadmk_proj REAL NOT NULL,
        bjp_proj REAL NOT NULL,
        tvk_lead REAL NOT NULL,
        status TEXT NOT NULL,
        top_issue TEXT NOT NULL,
        voter_salience INTEGER NOT NULL,
        tvk_messaging INTEGER NOT NULL,
        gap INTEGER NOT NULL,
        confidence INTEGER NOT NULL,
        source_name TEXT NOT NULL,
        source_url TEXT NOT NULL,
        methodology TEXT NOT NULL,
        whatsapp TEXT NOT NULL,
        instagram TEXT NOT NULL,
        twitter TEXT NOT NULL
    )
    """)

    # 3. GCC Wards Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS gcc_wards (
        unit_id TEXT PRIMARY KEY,
        ward_number INTEGER NOT NULL,
        name TEXT NOT NULL,
        zone_name TEXT NOT NULL,
        region TEXT NOT NULL,
        lat REAL NOT NULL,
        lon REAL NOT NULL,
        voters INTEGER NOT NULL,
        tvk_fav REAL NOT NULL,
        dmk_fav REAL NOT NULL,
        aiadmk_fav REAL NOT NULL,
        bjp_fav REAL NOT NULL,
        tvk_lead REAL NOT NULL,
        status TEXT NOT NULL,
        top_issue TEXT NOT NULL,
        voter_salience INTEGER NOT NULL,
        tvk_messaging INTEGER NOT NULL,
        gap INTEGER NOT NULL,
        confidence INTEGER NOT NULL,
        source_name TEXT NOT NULL,
        source_url TEXT NOT NULL,
        methodology TEXT NOT NULL,
        whatsapp TEXT NOT NULL,
        instagram TEXT NOT NULL,
        twitter TEXT NOT NULL
    )
    """)

    # 4. Issue Mining Events (6-Month Social & News Stream Feb-Aug 2026)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS issue_events (
        event_id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        platform TEXT NOT NULL,
        source_channel TEXT NOT NULL,
        raw_text TEXT NOT NULL,
        geo_location TEXT NOT NULL,
        assigned_district TEXT NOT NULL,
        category TEXT NOT NULL,
        spam_score REAL NOT NULL,
        is_verified INTEGER NOT NULL,
        sentiment_score REAL NOT NULL,
        source_url TEXT NOT NULL
    )
    """)

    # 5. Spam Audit Log Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS spam_filter_logs (
        log_id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        platform TEXT NOT NULL,
        raw_content TEXT NOT NULL,
        reason TEXT NOT NULL,
        action_taken TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()
    print("✅ Database nethra_campaign.db initialized with clean schema!")

if __name__ == "__main__":
    init_db()
