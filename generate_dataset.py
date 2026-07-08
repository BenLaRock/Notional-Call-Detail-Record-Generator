import importlib
# cdr creation utils
from creation_utils.subscribers import generate_subscribers
from creation_utils.contacts import build_contact_graph
from creation_utils.towers import generate_towers
from creation_utils.events import generate_cdr_events
from creation_utils.exporters import export_cdr
# cdr validation utils
from validation_utils.summary import build_summaries, export_summaries
from validation_utils.edge_table import build_edge_list, export_edges
from validation_utils.validation import validate_all, export_validation_report

constants_module = importlib.import_module('creation_utils.constants')

def finalize(subscriber_events_map):
    # summaries
    summaries = build_summaries(subscriber_events_map)
    export_summaries(summaries)

    # edge table
    edges_rollup = build_edge_list(subscriber_events_map)
    export_edges(edges_rollup)

    # validation
    report = validate_all(subscriber_events_map)
    export_validation_report(report)
    return

def main():
    subscribers = generate_subscribers(constants_module, use_provided=True, output_seeds=True)
    (all_contacts, subscribers) = build_contact_graph(subscribers)
    towers = generate_towers()

    # map subscriber ID to subscriber object
    id_to_subscriber_map = {s.sid: s for s in subscribers}

    # attach actual subscriber objects to contact graph
    enriched_contacts = []
    for source_id, target_id, freq in all_contacts:
        enriched_contacts.append((id_to_subscriber_map[source_id], id_to_subscriber_map[target_id]))

    # generate CDRs
    subscriber_events_map = {}
    for subscriber in subscribers:
        # get only that subscriber's contacts
        relevant_contacts = [
            t for (s, t) in enriched_contacts if s.sid == subscriber.sid
        ]
        events = generate_cdr_events(subscriber, relevant_contacts[:], towers)
        if not events:
            continue

        subscriber_events_map.update({subscriber.sid: events})
        export_cdr(subscriber, events)

    finalize(subscriber_events_map)
    print('CDR generation complete')
    return

if __name__ == '__main__':
    main()