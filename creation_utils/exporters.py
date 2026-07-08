import csv
import os
import json
from creation_utils.constants import TOP_LEVEL_OUTPUT_DIR, CDR_OUTPUT_DIR, EXTRAS_OUTPUT_DIR
from datetime import datetime

NOW_STRFTIME = datetime.today().strftime('%Y-%m-%d@%H%M')
OUTPUT_DIR_NAME = f'{TOP_LEVEL_OUTPUT_DIR}_{NOW_STRFTIME}'
FULL_CDR_OUTPUT_DIR = f'{OUTPUT_DIR_NAME}/{CDR_OUTPUT_DIR}'
FULL_EXTRAS_OUTPUT_DIR = f'{OUTPUT_DIR_NAME}/{EXTRAS_OUTPUT_DIR}'

# ---------- Creation utils exporters
def create_output_dir():    
    os.makedirs(OUTPUT_DIR_NAME)

def export_seed_subscribers(subscribers):
    os.makedirs(FULL_EXTRAS_OUTPUT_DIR, exist_ok=True)
    filename = f'{FULL_EXTRAS_OUTPUT_DIR}/seed_subscribers.json'
    with open(filename, 'w') as f:
        json.dump(subscribers, f, indent=4)
    return 

def export_cdr(subscriber, events):
    os.makedirs(FULL_CDR_OUTPUT_DIR, exist_ok=True)
    filename = f'{FULL_CDR_OUTPUT_DIR}/{subscriber.sid}_CDR.csv'
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=events[0].keys())
        writer.writeheader()
        writer.writerows(events)
    return

# ---------- Validation utils exporters
def export_summaries(rows):
    os.makedirs(FULL_EXTRAS_OUTPUT_DIR, exist_ok=True)
    filename = f'{FULL_EXTRAS_OUTPUT_DIR}/summaries.csv'
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    return

def export_edges(edge_counter):
    os.makedirs(FULL_EXTRAS_OUTPUT_DIR, exist_ok=True)
    filename = f'{FULL_EXTRAS_OUTPUT_DIR}/edges_rollup.csv'
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Source', 'Target', 'Weight'])
        for (src, dst), w in edge_counter.items():
            writer.writerow([src, dst, w])
    return

def export_validation_report(report):
    os.makedirs(FULL_EXTRAS_OUTPUT_DIR, exist_ok=True)
    filename = f'{FULL_EXTRAS_OUTPUT_DIR}/validation_report.txt'
    with open(filename, 'w') as f:
        if not report:
            f.write('Dataset is valid\n')
        else:
            for sid, issues in report:
                f.write(f'{sid}:\n')
                for i in issues:
                    f.write(f'  - {i}\n')
    return