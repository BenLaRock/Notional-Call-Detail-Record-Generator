import csv
import os
import json
from creation_utils.constants import FULL_CDR_OUTPUT_DIR

def export_seed_subscribers(subscribers):
    os.makedirs(FULL_CDR_OUTPUT_DIR)
    filename = f"{FULL_CDR_OUTPUT_DIR}/seed_subscribers.json"
    with open(filename, "w") as f:
        json.dump(subscribers, f, indent=4)
    return 

def export_cdr(subscriber, events):
    os.makedirs(FULL_CDR_OUTPUT_DIR, exist_ok=True)
    filename = f"{FULL_CDR_OUTPUT_DIR}/{subscriber.sid}_CDR.csv"
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=events[0].keys())
        writer.writeheader()
        writer.writerows(events)
    return