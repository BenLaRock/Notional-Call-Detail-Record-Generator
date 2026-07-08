import random

def assign_mobility_rules(subscriber):
    '''
    Defines which tower pools a subscriber can access.
    '''
    if subscriber.role == 'MX_DTO_LEADERSHIP':
        return {
            'home': 'MX',
            'allowed': ['MX'],   # stays in Mexico
            'cross_border': False
        }
    if subscriber.role == 'CROSS_BORDER_DRIVER':
        return {
            'home': subscriber.country,
            'allowed': ['MX', 'US'],  # crosses border regularly
            'cross_border': True
        }
    if subscriber.role == 'US_DISTRIBUTOR':
        return {
            'home': 'US',
            'allowed': ['US'],  # stays in US
            'cross_border': False
        }
    if subscriber.role == 'US_PICKUP_DRIVER':
        return {
            'home': 'US',
            'allowed': ['US'],
            'cross_border': False
        }
    return {'home': 'US', 'allowed': ['US'], 'cross_border': False}


def select_tower(towers, allowed_regions):
    filtered = [t for t in towers if t[4] in allowed_regions]
    return random.choice(filtered)