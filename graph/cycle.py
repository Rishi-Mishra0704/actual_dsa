from graph.adj import build_adj


def dfs(i, parent, adj, visited):
    visited[i] = True

    for x in adj[i]:
        if x == parent:
            continue  # the edge we just came along, not a cycle
        if visited[x]:
            return True  # a second path to x, so there is a cycle
        if dfs(x, i, adj, visited):
            return True
    return False


def has_cycle(n, adj):
    visited = [False] * n
    # start from every unvisited node so disconnected parts are checked too
    for i in range(n):
        if not visited[i] and dfs(i, -1, adj, visited):
            return True
    return False


n = 6
tree = [[0, 1], [0, 2], [1, 3], [2, 4], [3, 5]]
cyclic = tree + [[4, 5]]  # closes the loop 0-1-3-5-4-2-0

print("tree:  ", has_cycle(n, build_adj(n, tree)))
print("cyclic:", has_cycle(n, build_adj(n, cyclic)))
