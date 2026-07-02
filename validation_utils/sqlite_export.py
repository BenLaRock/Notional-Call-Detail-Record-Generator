# sqlite_export.py

import sqlite3

def export_to_sqlite(all_events):
    conn = sqlite3.connect("output/cdr.db")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS cdr (
            RecordID TEXT,
            SubscriberID TEXT,
            EventTimestamp TEXT,
            Direction TEXT,
            EventType TEXT,
            CallingNumber TEXT,
            CalledNumber TEXT,
            DurationSec INTEGER,
            SMSLength INTEGER,
            CellTowerID TEXT,
            Latitude REAL,
            Longitude REAL
        )
    """)

    for events in all_events.values():
        for e in events:
            c.execute("""
                INSERT INTO cdr VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                e["RecordID"],
                e["SubscriberID"],
                e["EventTimestamp"],
                e["Direction"],
                e["EventType"],
                e["CallingNumber"],
                e["CalledNumber"],
                e.get("DurationSec", 0),
                e.get("SMSLength", 0),
                e["CellTowerID"],
                e["Latitude"],
                e["Longitude"]
            ))

    conn.commit()
    conn.close()