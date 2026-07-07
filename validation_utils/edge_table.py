import csv
from collections import Counter
import os
from creation_utils.constants import FULL_EXTRAS_OUTPUT_DIR

def build_edge_list(all_events):
    """
    Counts all edges (voice or SMS) for a given source-target pair
    and returns the aggregate edge count.
    """
    edge_counter = Counter()
    for events in all_events.values():
        for e in events:
            src = e["CallingNumber"]
            dst = e["CalledNumber"]
            key = (src, dst)
            edge_counter[key] += 1
    return edge_counter

def export_edges(edge_counter):
    os.makedirs(FULL_EXTRAS_OUTPUT_DIR, exist_ok=True)
    filename = f"{FULL_EXTRAS_OUTPUT_DIR}/edges_rollup.csv"
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Source", "Target", "Weight"])
        for (src, dst), w in edge_counter.items():
            writer.writerow([src, dst, w])
    return