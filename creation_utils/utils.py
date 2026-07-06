import random
import string
from datetime import timedelta
from creation_utils.config import START_DATE, END_DATE, US_AREA_CODES

def random_phone_us(area_code=None):
    if not area_code:
        area_code = random.choice(US_AREA_CODES)
    return f"+1{area_code}{random.randint(200,999)}{random.randint(1000,9999)}"

def random_phone_mx():
    return f"+52{random.randint(1000000000, 9999999999)}"

def random_id(prefix="ID"):
    return f"{prefix}-{random.randint(100000,999999)}"

def random_timestamp():
    delta = END_DATE - START_DATE
    seconds = random.randint(0, int(delta.total_seconds()))
    return START_DATE + timedelta(seconds=seconds)

def random_string(n=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=n))

COUNTRY_PHONE_MAP = {
    "MX": random_phone_mx,
    "US": random_phone_us,
}