from graph.adj import build_adj
from stack_queue.queue import Queue
from stack_queue.stack import Stack


def bfs(adj, start):
    visited = [False] * len(adj)
    ans = []  # nodes in the order they are visited

    q = Queue()
    q.push(start)
    visited[start] = True

    while q.size() > 0:
        node = q.pop()  # oldest node, from the front
        ans.append(node)
        for x in adj[node]:
            if not visited[x]:
                visited[x] = True  # mark when queued so x is never queued twice
                q.push(x)
    return ans


def dfs(adj, start):
    visited = [False] * len(adj)
    ans = []  # nodes in the order they are visited

    stack = Stack()
    stack.push(start)

    while stack.size() > 0:
        node = stack.pop()  # newest node, from the top
        if visited[node]:
            continue  # a node can be pushed more than once; skip repeats
        visited[node] = True  # mark when popped, so the order follows the depth
        ans.append(node)
        for x in reversed(adj[node]):  # reversed so the first neighbour is popped first
            if not visited[x]:
                stack.push(x)
    return ans


# number of nodes (labelled 0 to n-1) and the edges between them
n = 6
edges = [[0, 1], [0, 2], [1, 3], [2, 4], [3, 5], [4, 5]]
adj = build_adj(n, edges)

print("BFS:", bfs(adj, 0))
print("DFS:", dfs(adj, 0))
