# graph_export.py

import csv
from collections import Counter

def build_edge_list(all_events):
    edge_counter = Counter()

    for events in all_events.values():
        for e in events:
            src = e["CallingNumber"]
            dst = e["CalledNumber"]

            key = (src, dst)
            edge_counter[key] += 1

    return edge_counter


def export_edges(edge_counter):
    with open("output/edges.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Source", "Target", "Weight"])

        for (src, dst), w in edge_counter.items():
            writer.writerow([src, dst, w])