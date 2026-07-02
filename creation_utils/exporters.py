import csv
import os
import json

OUTPUT_DIR = 'cdr_outputs'

def export_subscribers(subscribers):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filename = f"{OUTPUT_DIR}/subscribers.json"
    with open(filename, "w") as f:
        json.dump(subscribers, f, indent=4)

def export_cdr(subscriber, events):
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filename = f"{OUTPUT_DIR}/{subscriber.sid}_CDR.csv"
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=events[0].keys())
        writer.writeheader()
        writer.writerows(events)

