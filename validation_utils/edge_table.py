from collections import Counter

def build_edge_list(all_events):
    '''
    Counts all edges (voice or SMS) for a given source-target pair
    and returns the aggregate edge count.
    '''
    edge_counter = Counter()
    for events in all_events.values():
        for e in events:
            src = e['CallingNumber']
            dst = e['CalledNumber']
            key = (src, dst)
            edge_counter[key] += 1
    return edge_counter