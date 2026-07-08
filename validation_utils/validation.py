def validate_cdr(events):
    issues = []
    for e in events:
        if not e['CellTowerID']:
            issues.append('Missing tower ID')
        if e['EventType'] not in ['VOICE', 'SMS']:
            issues.append('Invalid event type')
        if not e['CallingNumber'] or not e['CalledNumber']:
            issues.append('Missing phone numbers')
    return issues


def validate_all(subscriber_events_map):
    report = []
    for sid, events in subscriber_events_map.items():
        issues = validate_cdr(events)
        if issues:
            report.append((sid, issues))
    return report