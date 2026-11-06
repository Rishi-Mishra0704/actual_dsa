from collections import defaultdict, deque

def topo_sort_kahn(num_nodes, edges):
    # edges: (before, after) means "before" must come first
    graph = defaultdict(list)
    in_degree = [0] * num_nodes          # how many prerequisites each node still waits on
    for before, after in edges:
        graph[before].append(after)
        in_degree[after] += 1

    # start with nodes that have no prerequisites
    queue = deque(node for node in range(num_nodes) if in_degree[node] == 0)
    order = []

    while queue:
        node = queue.popleft()
        order.append(node)
        for next_node in graph[node]:
            in_degree[next_node] -= 1    # one prerequisite done
            if in_degree[next_node] == 0:
                queue.append(next_node)  # all prerequisites done, ready

    if len(order) != num_nodes:          # some nodes never reached 0 = cycle
        return []
    return order