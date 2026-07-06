import random
from creation_utils.exporters import export_subscribers
import os
import json
from pathlib import Path
from creation_utils.config import ARCHETYPES
from creation_utils.utils import COUNTRY_PHONE_MAP
from creation_utils.subscribers import Subscriber

def generate_subscribers(config, use_provided=False, output=False):
    """
    Either load existing subscribers from JSON if provided or create new.
    """
    if use_provided:
        subscribers = load_subscribers()
    else:
        subscribers = create_subscribers(config)
    
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
    Check 'subscribers.json' in project root directory and load existing subscriber data.
    """

    # Get directory of current script, then target file at project root
    root_dir = Path(__file__).resolve().parent.parent 
    try:
        found_json_filename = [
            f for f in os.listdir() if f.endswith('json') and 'subscribers' in f
            ][0]
    except IndexError:
        raise FileNotFoundError("No subscribers.json file in project root directory")
    full_json_path = fr"{root_dir}\{found_json_filename}"
    with open(full_json_path, "r") as f:
        subscribers = json.load(f)
    return init_subscribers(subscribers)

def init_subscribers(raw):
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
        

def create_subscribers(config):
    subscribers = []

    for a in config.ARCHETYPES:
        arch_role = config.ARCHETYPES[a]["role"]
        arch_max_allowed = config.ARCHETYPES[a]["role_max_allowed"]

        for i in range(arch_max_allowed):
            arch_id_prefix = config.ARCHETYPES[a]["role_id_prefix"]
            arch_sid =f'{arch_id_prefix}{i+1:03d}'
            arch_country = random.choice(config.ARCHETYPES[a]["role_countries"])
            arch_phone = COUNTRY_PHONE_MAP[arch_country]()

            subscribers.append(
                config.ARCHETYPES[a]["create"](
                    sid=arch_sid, 
                    role=arch_role,
                    country=arch_country, 
                    phone=arch_phone
                )
            )
    return subscribers