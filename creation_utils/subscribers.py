import random
import os
import json
from pathlib import Path
from creation_utils.exporters import export_seed_subscribers
from creation_utils.constants import ARCHETYPES, Subscriber
from creation_utils.utils import random_phone_matching_country

def generate_subscribers(config, use_provided=False, output_seeds=False):
    '''
    Load existing seed subscribers from JSON if provided or create new seed subscribers.
    '''
    if use_provided:
        subscribers = load_subscribers()
    else:
        subscribers = create_subscribers(config)
    
    if output_seeds:
        subscribers_output = [{
                'role': s.role,
                'id': s.sid, 
                'phone': s.phone, 
                'country': s.country
            } for s in subscribers]
        export_seed_subscribers(subscribers_output)
    return subscribers

def load_subscribers():
    '''
    Check for 'subscribers.json' in project root directory and load existing subscriber data.
    '''
    # Get directory of current script, then target file at project root
    root_dir = Path(__file__).resolve().parent.parent 
    try:
        found_json_filename = [f for f in os.listdir() if f.endswith('json') and 'subscribers' in f][0]
    except IndexError:
        raise FileNotFoundError('No subscribers.json file in project root directory')
    
    full_json_path = fr'{root_dir}\{found_json_filename}'
    with open(full_json_path, 'r') as f:
        subscribers = json.load(f)
    return init_subscribers(subscribers)

def init_subscribers(raw):
    subscribers = []
    for r in raw:
        subscribers.append(
            Subscriber(
                sid=r['id'],
                role=r['role'],
                phone=r['phone'],
                country=r['country']
            )
        )
    return subscribers
        

def create_subscribers(config):
    subscribers = []
    for archetype in config.ARCHETYPES:
        archetype_role = config.ARCHETYPES[archetype]['role']
        archetype_max_allowed = config.ARCHETYPES[archetype]['role_max_allowed']

        for i in range(archetype_max_allowed):
            archetype_id_prefix = config.ARCHETYPES[archetype]['role_id_prefix']
            archetype_sid =f'{archetype_id_prefix}{i+1:03d}'
            archetype_country = random.choice(config.ARCHETYPES[archetype]['role_countries'])
            archetype_phone = random_phone_matching_country(archetype_country)

            subscribers.append(
                config.ARCHETYPES[archetype]['create'](
                    sid=archetype_sid, 
                    role=archetype_role,
                    country=archetype_country, 
                    phone=archetype_phone
                )
            )
    return subscribers