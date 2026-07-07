from collections import defaultdict
import csv
import os
from creation_utils.constants import FULL_EXTRAS_OUTPUT_DIR

def summarize(events):
    summary = defaultdict(int)

    for e in events:
        summary["total_events"] += 1
        summary[e["EventType"]] += 1

        if e["Direction"] == "MO":
            summary["outgoing"] += 1
        elif e["Direction"] == "MT":
            summary["incoming"] += 1

    return summary


def build_summaries(subscriber_event_map):
    rows = []
    for sid, events in subscriber_event_map.items():
        s = summarize(events)

        rows.append({
            "SubscriberID": sid,
            "TotalEvents": s["total_events"],
            "Voice": s.get("VOICE", 0),
            "SMS": s.get("SMS", 0),
            "Outgoing": s["outgoing"],
            "Incoming": s["incoming"]
        })

    return rows


def export_summaries(rows):
    os.makedirs(FULL_EXTRAS_OUTPUT_DIR, exist_ok=True)
    filename = f"{FULL_EXTRAS_OUTPUT_DIR}/summaries.csv"
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    return