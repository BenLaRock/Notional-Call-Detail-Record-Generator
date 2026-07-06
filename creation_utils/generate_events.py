import random
from datetime import timedelta
from creation_utils.utils import random_timestamp, random_string
from creation_utils.mobility import assign_mobility_rules, select_tower
from creation_utils.config import VOICE_RATIO, MIN_EVENTS_PER_CONTACT, MAX_EVENTS_PER_CONTACT

def generate_cdr_events(subscriber, contacts, towers):
    """
    Generates a list of CDR events for one subscriber.
    """

    events = []
    rules = assign_mobility_rules(subscriber)

    print(len(contacts), 'contacts for subscriber ', subscriber.sid)
    for contact in contacts:
        # number of interactions per contact
        num_events = random.randint(MIN_EVENTS_PER_CONTACT, MAX_EVENTS_PER_CONTACT)

        for _ in range(num_events):

            timestamp = random_timestamp()

            is_voice = random.random() < VOICE_RATIO

            direction = random.choice(["MO", "MT"])

            tower = select_tower(towers, rules["allowed"])

            event = {
                "RecordID": random_string(10),
                "SubscriberID": subscriber.sid,
                "SubscriberRole": subscriber.role,
                "EventTimestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "Direction": direction,
                "EventType": "VOICE" if is_voice else "SMS",
                "CallingNumber": subscriber.phone if direction == "MO" else contact.phone,
                "CalledNumber": contact.phone if direction == "MO" else subscriber.phone,
                "DurationSec": random.randint(20, 600) if is_voice else "",
                "SMSLength": random.randint(10, 160) if not is_voice else "",
                "IMEI": random.randint(100000000000000, 999999999999999), # long term, should not be random
                "IMSI": random.randint(100000000000000, 999999999999999),
                "CellTowerID": tower[0],
                "TowerName": tower[1],
                "Latitude": tower[2],
                "Longitude": tower[3],
                "Country": tower[4],
            }

            events.append(event)

    return events