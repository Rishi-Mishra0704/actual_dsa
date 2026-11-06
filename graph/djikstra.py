import heapq
from math import inf

def dijkstra(num_nodes, edges, source):
    # neighbours[node] = list of (neighbour, weight), adj list
    neighbours = [[] for _ in range(num_nodes)]
    for from_node, to_node, weight in edges:
        neighbours[from_node].append((to_node, weight))

    # shortest distance found so far to each node
    shortest = [inf] * num_nodes
    shortest[source] = 0

    # min-heap of (distance_so_far, node), closest node comes out first
    heap = [(0, source)]

    while heap:
        current_dist, current_node = heapq.heappop(heap)

        # stale entry: we already found a shorter path to this node
        if current_dist > shortest[current_node]:
            continue

        for neighbour, weight in neighbours[current_node]:
            new_dist = current_dist + weight
            if new_dist < shortest[neighbour]:
                shortest[neighbour] = new_dist
                heapq.heappush(heap, (new_dist, neighbour))

    return shortest   # inf means unreachable

# cities 0..4, roads as (from, to, minutes)
edges = [
    (0, 1, 4),   # 0 -> 1 takes 4
    (0, 2, 1),   # 0 -> 2 takes 1
    (2, 1, 2),   # 2 -> 1 takes 2
    (1, 3, 1),   # 1 -> 3 takes 1
    (2, 3, 5),   # 2 -> 3 takes 5
]               # city 4 has no roads in

print(dijkstra(5, edges, 0))
# [0, 3, 1, 4, inf]