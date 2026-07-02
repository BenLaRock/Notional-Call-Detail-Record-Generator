# from pathlib import Path
# import sys
# # navigate up two levels to reach 'root_project/'
# root_dir = Path(__file__).resolve().parents[1]
# sys.path.append(str(root_dir))

# cdr creation utils
from creation_utils.subscribers import generate_subscribers
from creation_utils.subscribers import generate_subscribers
from creation_utils.contacts import build_contact_graph
from creation_utils.towers import generate_towers
from creation_utils.events import generate_cdr_events
from creation_utils.exporters import export_cdr
import importlib

# cdr validation utils
from validation_utils.analytics import build_summaries, write_summaries
from validation_utils.graph_export import build_edge_list, export_edges
from validation_utils.validation import validate_all, write_validation_report

config_module = importlib.import_module('creation_utils.config')

# def finalize(all_events):

#     # summaries
#     summaries = build_summaries(all_events)
#     write_summaries(summaries)

#     # graph
#     edges = build_edge_list(all_events)
#     export_edges(edges)

#     # validation
#     report = validate_all(all_events)
#     write_validation_report(report)

def main():

    subscribers = generate_subscribers(config_module, use_provided=True, output=False)
    print(len(subscribers))

    # contacts = build_contact_graph(subscribers)
    # print(len(contacts))
    # towers = generate_towers()

    # # map subscriberID → subscriber object
    # sub_map = {s.sid: s for s in subscribers}

    # # attach actual subscriber objects to contact graph
    # enriched_contacts = []

    # for source_id, target_id, freq in contacts:
    #     enriched_contacts.append((sub_map[source_id], sub_map[target_id]))
    # print(len(enriched_contacts))

    # # generate CDRs
    # for subscriber in subscribers:

    #     # # this may be problematic - there are only 19 unique calling/called numbers in concat dataset
    #     # relevant_contacts = [
    #     #     t for (s, t) in enriched_contacts if s.sid == subscriber.sid
    #     # ]
    #     relevant_contacts = [
    #         t for (s, t) in enriched_contacts
    #     ]
    #     print(relevant_contacts)

    #     events = generate_cdr_events(subscriber, relevant_contacts, towers)

    #     if events:
    #         export_cdr(subscriber, events)
    
    # # # validate final dataset
    # # finalize(all_events)

    # print("CDR generation complete.")

if __name__ == "__main__":
    main()