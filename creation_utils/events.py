import random
from datetime import timedelta
from creation_utils.utils import random_timestamp, random_string
from creation_utils.mobility import assign_mobility_rules, select_tower
from creation_utils.constants import VOICE_RATIO, MIN_EVENTS_PER_CONTACT, MAX_EVENTS_PER_CONTACT

PAIR_DIRECTIONALITY_OPTIONS = [
    'subscriber_to_contact',
    'contact_to_subscriber',
    'bidirectional'
]

def assign_event_direction(pair_directionality):
    match pair_directionality:
        case 'subscriber_to_contact':
            return 'MO'
        case 'contact_to_subscriber':
            return 'MT'
        case 'bidirectional':
            return random.choice(['MO', 'MT'])
        case _:
            return random.choice(['MO', 'MT'])

def generate_cdr_events(subscriber, contacts, towers):
    events = []
    rules = assign_mobility_rules(subscriber)
    if not contacts:
        return []
    for contact in contacts:
        # number of interactions per contact
        num_events = random.randint(MIN_EVENTS_PER_CONTACT, MAX_EVENTS_PER_CONTACT)
        # determine directionality for all events for current contact
        pair_directionality = random.choice(PAIR_DIRECTIONALITY_OPTIONS)
        for _ in range(num_events):
            timestamp = random_timestamp()
            is_voice = random.random() < VOICE_RATIO
            event_direction = assign_event_direction(pair_directionality)
            tower = select_tower(towers, rules['allowed'])
            event = {
                'RecordID': random_string(10),
                'SubscriberID': subscriber.sid,
                'SubscriberRole': subscriber.role,
                'EventTimestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'Direction': event_direction,
                'EventType': 'VOICE' if is_voice else 'SMS',
                'CallingNumber': subscriber.phone if event_direction == 'MO' else contact.phone,
                'CalledNumber': contact.phone if event_direction == 'MO' else subscriber.phone,
                'DurationSec': random.randint(20, 600) if is_voice else '',
                'SMSLength': random.randint(10, 160) if not is_voice else '',
                'IMEI': random.randint(100000000000000, 999999999999999),
                'IMSI': random.randint(100000000000000, 999999999999999),
                'CellTowerID': tower[0],
                'TowerName': tower[1],
                'Latitude': tower[2],
                'Longitude': tower[3],
                'Country': tower[4],
            }
            events.append(event)
    return events