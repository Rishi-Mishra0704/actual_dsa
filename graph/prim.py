from collections import defaultdict
import heapq

def prim(num_nodes, edges):
    graph = defaultdict(list)
    for a, b, w in edges:
        graph[a].append((b, w))
        graph[b].append((a, w))          # undirected

    in_tree = [False] * num_nodes
    heap = [(0, 0)]                      # (edge_weight, node), start from node 0
    total_cost = 0
    nodes_added = 0

    while heap and nodes_added < num_nodes:
        weight, node = heapq.heappop(heap)
        if in_tree[node]:                # stale: already connected more cheaply
            continue
        in_tree[node] = True
        total_cost += weight
        nodes_added += 1
        for neighbour, edge_weight in graph[node]:
            if not in_tree[neighbour]:
                heapq.heappush(heap, (edge_weight, neighbour))

    return total_cost if nodes_added == num_nodes else -1