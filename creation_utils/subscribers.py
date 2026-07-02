import random
from creation_utils.utils import random_id, random_phone_mx, random_phone_us
from creation_utils.exporters import export_subscribers
import os
import json
from pathlib import Path

class Subscriber:
    def __init__(self, sid, role, phone, country):
        self.sid = sid
        self.role = role
        self.phone = phone
        self.country = country
        self.contacts = []

def generate_subscribers(config, use_provided=False, output=False):
    if use_provided:
        raw_subscribers = load_subscribers()
        subscribers = transform_subscribers(raw_subscribers)
    else:
        subscribers = create_new_subscribers(config)
    
    if output:
        subscribers_output = [{
                'role': s.role,
                'id': s.sid, 
                'phone': s.phone, 
                'country': s.country
            } for s in subscribers]
        export_subscribers(subscribers_output)
    return subscribers

def load_subscribers():
    """
    Check for JSON file with 'subscribers' in filename in top-level directory of project and load existing subscriber data.
    """

    # Get the directory of the current script, then target the file at the project root
    root_dir = Path(__file__).resolve().parent.parent 
    
    try:
        found_json_filename = [f for f in os.listdir() if f.endswith('json') and 'subscribers' in f][0]
    except IndexError:
        raise FileNotFoundError("No subscribers JSON file present in project root directory")

    full_json_path = fr"{root_dir}\{found_json_filename}"
    with open(full_json_path, "r") as f:
        subscribers = json.load(f)
    return subscribers

def transform_subscribers(raw):
    subscribers = []
    for r in raw:
        subscribers.append(
            Subscriber(
                sid=r["id"],
                role=r["role"],
                phone=r["phone"],
                country=r["country"]
            )
        )

    return subscribers
        

def create_new_subscribers(config):
    subscribers = []

    # -------------------------
    # DTO Leaders (Sonora, MX)
    # -------------------------
    for i in range(config.NUM_MX_DTO_LEADERSHIP):
        subscribers.append(
            Subscriber(
                sid=f"DTO_LEADER{i+1:03d}",
                role="MX_DTO_LEADERSHIP",
                phone=random_phone_mx(),
                country="MX"
            )
        )

    # -------------------------
    # Cross-border Drivers (MX + US mix)
    # -------------------------
    for i in range(config.NUM_CROSS_BORDER_DRIVERS):
        country = random.choice(["MX", "US"])
        phone = random_phone_mx() if country == "MX" else random_phone_us()
        subscribers.append(
            Subscriber(
                sid=f"CROSS_BORDER_DRIVER{i+1:03d}",
                role="CROSS_BORDER_DRIVER",
                phone=phone,
                country=country
            )
        )

    # -------------------------
    # Distributors (CA and AZ, US)
    # -------------------------
    for i in range(config.NUM_US_DISTRIBUTORS):
        subscribers.append(
            Subscriber(
                sid=f"DISTRIBUTOR{i+1:03d}",
                role="US_DISTRIBUTOR",
                phone=random_phone_us(),
                country="US"
            )
        )

    # -------------------------
    # Pick-up Drivers (CA and AZ, US)
    # -------------------------
    for i in range(config.NUM_US_PICKUP_DRIVERS):
        subscribers.append(
            Subscriber(
                sid=f"PICKUP_DRIVER{i+1:03d}",
                role="US_PICKUP_DRIVER",
                phone=random_phone_us(),
                country="US"
            )
        )
    
    return subscribers