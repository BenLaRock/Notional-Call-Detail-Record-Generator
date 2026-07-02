import random
from creation_utils.config import MIN_CONTACTS, MAX_CONTACTS

def pick_contacts(source, candidates, min_c=MIN_CONTACTS, max_c=MAX_CONTACTS):
    n = random.randint(min_c, max_c)
    return random.sample(candidates, min(n, len(candidates)))


def build_contact_graph(subscribers):
    contacts = []

    # Grouping
    DTO_LEADER = [s for s in subscribers if s.role == "MX_DTO_LEADERSHIP"]
    CROSS_BORDER_DRIVER = [s for s in subscribers if s.role == "CROSS_BORDER_DRIVER"]
    DISTRIBUTOR = [s for s in subscribers if s.role == "US_DISTRIBUTOR"]
    PICKUP_DRIVER = [s for s in subscribers if s.role == "US_PICKUP_DRIVER"]

    # -------------------------
    # RULES ENFORCED
    # -------------------------

    for dto_leader in DTO_LEADER:
        # DTO_LEADER ↔ CROSS_BORDER_DRIVER (regular)
        dto_leader.contacts += CROSS_BORDER_DRIVER
        for cross_border_driver in CROSS_BORDER_DRIVER:
            contacts.append((dto_leader.sid, cross_border_driver.sid, "REGULAR"))

        # DTO_LEADER ↔ DISTRIBUTOR (sporadic)
        for distributor in random.sample(DISTRIBUTOR, max(1, len(DISTRIBUTOR)//2)):
            dto_leader.contacts.append(distributor)
            contacts.append((dto_leader.sid, distributor.sid, "SPORADIC"))

    for cross_border_driver in CROSS_BORDER_DRIVER:
        # CROSS_BORDER_DRIVER ↔ DTO_LEADER (infrequent)
        for dto_leader in random.sample(DTO_LEADER, 1):
            contacts.append((cross_border_driver.sid, dto_leader.sid, "INFREQUENT"))

        # CROSS_BORDER_DRIVER ↔ DISTRIBUTOR (sporadic)
        for distributor in random.sample(DISTRIBUTOR, max(1, len(DISTRIBUTOR)//2)):
            contacts.append((cross_border_driver.sid, distributor.sid, "SPORADIC"))

    for distributor in DISTRIBUTOR:
        # DISTRIBUTOR ↔ DTO_LEADER (sporadic)
        for dto_leader in random.sample(DTO_LEADER, 1):
            contacts.append((distributor.sid, dto_leader.sid, "SPORADIC"))

        # DISTRIBUTOR ↔ CROSS_BORDER_DRIVER (sporadic)
        for cross_border_driver in random.sample(CROSS_BORDER_DRIVER, max(1, len(CROSS_BORDER_DRIVER)//2)):
            contacts.append((distributor.sid, cross_border_driver.sid, "SPORADIC"))

        # DISTRIBUTOR ↔ PICKUP_DRIVER (regular)
        for pickup_driver in PICKUP_DRIVER:
            contacts.append((distributor.sid, pickup_driver.sid, "REGULAR"))

    for pickup_driver in PICKUP_DRIVER:
        # PICKUP_DRIVER ONLY ↔ DISTRIBUTOR (regular)
        for distributor in DISTRIBUTOR:
            contacts.append((pickup_driver.sid, distributor.sid, "REGULAR"))

    return contacts