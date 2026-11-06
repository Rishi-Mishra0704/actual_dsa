from graph.adj import build_adj
from stack_queue.queue import Queue
from stack_queue.stack import Stack


def bfs(adj, start):
    # 1. visited list, all False
    visited = [False] * len(adj)
    # 2. visit order
    ans = []

    # 3. queue with start
    q = Queue()
    q.push(start)
    # 4. mark start visited
    visited[start] = True

    # 5. loop until queue is empty
    while q.size() > 0:
        # 6. take the oldest node, append to answer
        node = q.pop()
        ans.append(node)
        # 7. check each neighbour
        for x in adj[node]:
            if not visited[x]:
                # 8. mark on push so it's never queued twice
                visited[x] = True
                q.push(x)
    # 9. return the order
    return ans


def dfs(adj, start):
    # 1. visited list, all False
    visited = [False] * len(adj)
    # 2. visit order
    ans = []

    # 3. stack with start
    stack = Stack()
    stack.push(start)

    # 4. loop until stack is empty
    while stack.size() > 0:
        # 5. take the newest node
        node = stack.pop()
        # 6. skip if already visited (can be pushed twice)
        if visited[node]:
            continue
        # 7. mark on pop so order follows depth
        visited[node] = True
        ans.append(node)
        # 8. push neighbours reversed so the first is popped first
        for x in reversed(adj[node]):
            if not visited[x]:
                stack.push(x)
    # 9. return the order
    return ans


# number of nodes (labelled 0 to n-1) and the edges between them
n = 6
edges = [[0, 1], [0, 2], [1, 3], [2, 4], [3, 5], [4, 5]]
adj = build_adj(n, edges)

print("BFS:", bfs(adj, 0))
print("DFS:", dfs(adj, 0))
