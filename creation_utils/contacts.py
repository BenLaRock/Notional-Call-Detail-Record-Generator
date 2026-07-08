import random
from creation_utils.constants import ARCHETYPES
from creation_utils.utils import random_id, random_phone_matching_country

def build_contact_graph(subscribers):
    contacts = []

    # Grouping
    DTO_LEADER = [s for s in subscribers if s.role == 'MX_DTO_LEADER']
    CROSS_BORDER_DRIVER = [s for s in subscribers if s.role == 'CROSS_BORDER_DRIVER']
    DISTRIBUTOR = [s for s in subscribers if s.role == 'US_DISTRIBUTOR']
    PICKUP_DRIVER = [s for s in subscribers if s.role == 'US_PICKUP_DRIVER']

    for dto_leader in DTO_LEADER:
        # Create edges for DTO leaders <> all cross-border drivers
        for cross_border_driver in CROSS_BORDER_DRIVER:
            cbd_edge = (dto_leader.sid, cross_border_driver.sid, 'REGULAR')
            contacts.append(cbd_edge)

        # Create edges for DTO leaders <> some distributors
        for distributor in random.sample(DISTRIBUTOR, max(1, len(DISTRIBUTOR)//2)):
            distributor_edge = (dto_leader.sid, distributor.sid, 'SPORADIC')
            contacts.append(distributor_edge)

        # Create non-DTO contacts
        new_contacts = create_random_contacts(dto_leader, 'MX_DTO_LEADER', subscribers)
        contacts.extend(new_contacts)

    for cross_border_driver in CROSS_BORDER_DRIVER:
        # Create edges for cross-border drivers <> a DTO leader
        for dto_leader in random.sample(DTO_LEADER, 1):
            contacts.append((cross_border_driver.sid, dto_leader.sid, 'INFREQUENT'))

        # Create edges for cross-border drivers <> some distributors
        for distributor in random.sample(DISTRIBUTOR, max(1, len(DISTRIBUTOR)//2)):
            contacts.append((cross_border_driver.sid, distributor.sid, 'SPORADIC'))

        # Create non-DTO contacts
        new_contacts = create_random_contacts(cross_border_driver, 'CROSS_BORDER_DRIVER', subscribers)
        contacts.extend(new_contacts)

    for distributor in DISTRIBUTOR:
        # Create edges for distributors <> a DTO leader
        for dto_leader in random.sample(DTO_LEADER, 1):
            contacts.append((distributor.sid, dto_leader.sid, 'SPORADIC'))

        # Create edges for distributors <> some cross-border drivers
        for cross_border_driver in random.sample(CROSS_BORDER_DRIVER, max(1, len(CROSS_BORDER_DRIVER)//2)):
            contacts.append((distributor.sid, cross_border_driver.sid, 'SPORADIC'))

        # Create edges for distributors <> all pickup drivers
        for pickup_driver in PICKUP_DRIVER:
            contacts.append((distributor.sid, pickup_driver.sid, 'REGULAR'))
    
        # Create non-DTO contacts
        new_contacts = create_random_contacts(distributor, 'US_DISTRIBUTOR', subscribers)
        contacts.extend(new_contacts)

    for pickup_driver in PICKUP_DRIVER:
        # Create edges for pickup drivers <> all distributors
        for distributor in DISTRIBUTOR:
            contacts.append((pickup_driver.sid, distributor.sid, 'REGULAR'))
    
        # Create non-DTO contacts
        new_contacts = create_random_contacts(pickup_driver, 'US_PICKUP_DRIVER', subscribers)
        contacts.extend(new_contacts)

    return (contacts, subscribers)


def create_random_contacts(source_subscriber, archetype_name, subscribers):
    curr_archetype = ARCHETYPES[archetype_name]
    min_contacts = ARCHETYPES[archetype_name]['contacts_min_allowed']
    max_contacts = ARCHETYPES[archetype_name]['contacts_max_allowed']
    num_contacts = random.randint(min_contacts, max_contacts)
    new_contact_edges = []
    for _ in range(num_contacts):
        contact_id_prefix = curr_archetype['contacts_id_prefix']
        contact_sid = random_id(contact_id_prefix)
        contact_country = random.choice(curr_archetype['contacts_countries'])
        contact_phone = random_phone_matching_country(contact_country)
        contact_frequency = random.choice(curr_archetype['contacts_frequencies'])

        # Create new subscriber object and updated original subscribers list
        contact_subscriber= curr_archetype['create'](
            sid=contact_sid,
            role='CONTACT',
            country=contact_country,
            phone=contact_phone
        )
        subscribers.append(contact_subscriber)
        contact_edge = (source_subscriber.sid, contact_subscriber.sid, contact_frequency)
        new_contact_edges.append(contact_edge)

    return new_contact_edges