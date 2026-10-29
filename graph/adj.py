def build_adj(n, edges):
    # adjacency list: adj[u] holds every neighbour of u
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)  # undirected, so add the edge both ways
    return adj
