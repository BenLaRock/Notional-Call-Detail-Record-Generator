import os
from creation_utils.constants import FULL_EXTRAS_OUTPUT_DIR

def validate_cdr(events):
    issues = []
    for e in events:
        if not e["CellTowerID"]:
            issues.append("Missing tower ID")
        if e["EventType"] not in ["VOICE", "SMS"]:
            issues.append("Invalid event type")
        if not e["CallingNumber"] or not e["CalledNumber"]:
            issues.append("Missing phone numbers")
    return issues


def validate_all(subscriber_events_map):
    report = []
    for sid, events in subscriber_events_map.items():
        issues = validate_cdr(events)
        if issues:
            report.append((sid, issues))
    return report


def export_validation_report(report):
    os.makedirs(FULL_EXTRAS_OUTPUT_DIR, exist_ok=True)
    filename = f"{FULL_EXTRAS_OUTPUT_DIR}/validation_report.txt"
    with open(filename, "w") as f:
        if not report:
            f.write("Dataset is valid\n")
        else:
            for sid, issues in report:
                f.write(f"{sid}:\n")
                for i in issues:
                    f.write(f"  - {i}\n")
    return