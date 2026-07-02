from datetime import datetime

# ----------------------------
# Dataset Scope
# ----------------------------

START_DATE = datetime(2026, 1, 1)
END_DATE   = datetime(2026, 6, 30)

SEED = 42  # reproducibility

# ----------------------------
# Archetype counts
# ----------------------------

# NUM_REGIONAL_MANAGERS = 3
# NUM_CROSS_BORDER_DRIVERS = 6
# NUM_DC_MANAGERS = 4
# NUM_LOCAL_DRIVERS = 6

NUM_MX_DTO_LEADERSHIP = 3
NUM_CROSS_BORDER_DRIVERS = 6
NUM_US_DISTRIBUTORS = 4
NUM_US_PICKUP_DRIVERS = 6

# ----------------------------
# Contact structure
# ----------------------------

MIN_CONTACTS = 30
MAX_CONTACTS = 100

MIN_EVENTS_PER_CONTACT = 3
MAX_EVENTS_PER_CONTACT = 21

# ----------------------------
# Event composition
# ----------------------------

VOICE_RATIO = 0.6
SMS_RATIO = 0.4

# ----------------------------
# Geography constraints
# ----------------------------

MEXICO_COUNTRY_CODE = "+52"
US_COUNTRY_CODE = "+1"

US_AREA_CODES = [
    "213", # CA Los Angeles downtown
    "310", # CA Los Angeles county 
    "323", # CA Los Angeles central
    "602", # AZ Phoenix
    "520", # AZ southern, greater Tucson
]

SONORA_TOWNS = ["Hermosillo", "Nogales", "Obregon", "Guaymas"]

US_TOWNS = ["Los Angeles", "Phoenix", "Tucson"]

# ----------------------------
# Cell tower definitions
# ----------------------------

# Sonora, MX
CELL_TOWERS_MX = [
    ("SN001", "Hermosillo Centro", 29.0892, -110.9613, "MX"),
    ("SN002", "Hermosillo Norte", 29.1261, -110.9554, "MX"),
    ("SN003", "Nogales MX", 31.3082, -110.9381, "MX"),
    ("SN004", "Ciudad Obregon", 27.4828, -109.9304, "MX"),
    ("SN005", "Guaymas Port", 27.9186, -110.8975, "MX"),
]
# California, US
CELL_TOWERS_US_CA = [
    ("US201", "San Diego East", 32.7157, -117.1611, "US"),
    ("US202", "San Diego Border Zone", 32.5421, -117.0318, "US"),
    ("US203", "Los Angeles Downtown", 34.0522, -118.2437, "US"),
    ("US204", "LA South Bay", 33.9019, -118.4173, "US"),
]
# Arizona, US
CELL_TOWERS_US_AZ = [
    ("US101", "Nogales AZ East", 31.3401, -110.9346, "US"),
    ("US102", "Tucson Central", 32.2226, -110.9747, "US"),
    ("US103", "Tucson South", 32.1810, -110.9650, "US"),
    ("US104", "Phoenix South", 33.4484, -112.0740, "US"),
    ("US105", "Phoenix West", 33.4480, -112.1030, "US"),
]
