# Graphs

Undirected graph as an adjacency list, breadth first search (BFS), depth first
search (DFS), and cycle detection.

| File | Contents |
|---|---|
| `adj.py` | `build_adj`, shared by the other two |
| `graph.py` | `bfs` with `Queue`, `dfs` with `Stack` (from `stack_queue/`) |
| `cycle.py` | `has_cycle` for undirected graphs, recursive DFS |

Run from the project root as modules, so the `graph` and `stack_queue` imports
resolve:

```
python -m graph.graph
python -m graph.cycle
```

`python graph/graph.py` fails with `ModuleNotFoundError: No module named
'stack_queue'`, because running a file directly only puts that file's own
folder (`graph/`) on the import path.

## The graph in graph.py

```python
n = 6
edges = [[0, 1], [0, 2], [1, 3], [2, 4], [3, 5], [4, 5]]
```

Six nodes labelled `0` to `5`, six edges. Drawn out:

```
        0
       / \
      1   2
      |   |
      3   4
       \ /
        5
```

There is no "first" or "root" node in a graph. `0` is drawn at the top only
because BFS starts there. Any node can be the start.

Notice the cycle `0 - 1 - 3 - 5 - 4 - 2 - 0`. Cycles are what separate a graph
from a tree, and they are the reason `visited` exists. A tree traversal never
reaches the same node twice; a graph traversal will, unless you stop it.

## Representation

The input format, a list of `[u, v]` pairs, is how problems hand you a graph.
It is useless for traversal: to find the neighbours of `3` you would scan every
edge. So the first step is always to convert it.

```python
def build_adj(n, edges):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    return adj
```

For the graph above:

```
adj[0] = [1, 2]
adj[1] = [0, 3]
adj[2] = [0, 4]
adj[3] = [1, 5]
adj[4] = [2, 5]
adj[5] = [3, 4]
```

`adj[u]` answers "where can I go from `u`?" in one lookup. That question is the
only one BFS and DFS ever ask.

### Why both directions

The edge `[0, 1]` means you can walk `0 -> 1` **and** `1 -> 0`. If you only
append `adj[u].append(v)`, node `1` has no idea it is connected to `0`, and a
search starting anywhere other than `0` misses edges.

For a **directed** graph, where `[u, v]` means one way only, delete the second
line. That is the entire difference.

### Why `[[] for _ in range(n)]` and not `[[]] * n`

```python
adj = [[]] * n   # WRONG
```

This creates **one** list and `n` references to it. Appending to `adj[0]`
appends to every slot, since they are all the same list. The comprehension
builds `n` separate lists.

### Variations

| Graph | Store in `adj[u]` |
|---|---|
| Undirected | `v`, added both ways |
| Directed | `v`, added one way |
| Weighted | `(v, w)` pairs |

An **adjacency matrix** (`n x n` grid, `matrix[u][v] = 1` if connected) is the
other common representation. O(1) to check whether a specific edge exists, but
O(n²) space even when there are few edges, and finding neighbours means scanning
a whole row. The list is the default for traversal.

## BFS

```python
def bfs(adj, start):
    visited = [False] * len(adj)
    ans = []

    q = Queue()
    q.push(start)
    visited[start] = True

    while q.size() > 0:
        node = q.pop()
        ans.append(node)
        for x in adj[node]:
            if not visited[x]:
                visited[x] = True
                q.push(x)
    return ans
```

`Queue.pop()` takes from the front. Internally it is a `deque` with
`popleft()`, so it is O(1).

`visited` and `ans` are created inside the function. When they were globals
shared by BFS and DFS, DFS started with every node already marked visited and
appended to BFS's leftover list, giving `[0, 1, 2, 3, 4, 5, 0]`. Each search
needs its own fresh state.

BFS explores outward in rings. Everything one edge from the start, then
everything two edges away, then three. The queue enforces that: nodes come out
in the order they went in, so a ring is fully processed before the next one
starts.

### Trace

```
queue           pop   neighbours   newly queued   ans
[0]             0     1, 2         1, 2           [0]
[1, 2]          1     0, 3         3              [0, 1]
[2, 3]          2     0, 4         4              [0, 1, 2]
[3, 4]          3     1, 5         5              [0, 1, 2, 3]
[4, 5]          4     2, 5         -              [0, 1, 2, 3, 4]
[5]             5     3, 4         -              [0, 1, 2, 3, 4, 5]
[]              loop ends
```

Output: `[0, 1, 2, 3, 4, 5]`.

Grouped by distance from `0`:

```
distance 0    0
distance 1    1, 2
distance 2    3, 4
distance 3    5
```

That layering is why BFS gives **shortest paths** in an unweighted graph. The
first time BFS reaches a node is via the fewest possible edges.

### Mark visited when queuing, not when popping

`visited[x] = True` happens the moment `x` enters the queue. Look at node `5`
in the trace: both `3` and `4` are its neighbours. If you only marked nodes
when popping them, `5` would still be unvisited when `4` is processed and it
would be queued a second time.

On this graph that means one duplicate. On a dense graph it can mean the queue
holds the same node many times over. Marking on entry guarantees each node is
queued exactly once.

## DFS

```python
def dfs(adj, start):
    visited = [False] * len(adj)
    ans = []

    stack = Stack()
    stack.push(start)

    while stack.size() > 0:
        node = stack.pop()
        if visited[node]:
            continue
        visited[node] = True
        ans.append(node)
        for x in reversed(adj[node]):
            if not visited[x]:
                stack.push(x)
    return ans
```

DFS goes as deep as it can down one path before backing up. Swapping the queue
for a stack is what does that: the newest node comes out first, so the search
keeps following the node it just discovered.

### Mark visited when popping, not when pushing

This is the opposite of BFS, and it is the part that is easy to get wrong.

Marking on push, the BFS way, still visits every node, but the recorded order is
not depth first. Popping `0` pushes and records **both** `1` and `2` before going
anywhere deep, so the output starts `[0, 1, 2, ...]`. That looks like BFS
because it is recording the order nodes were *discovered*, which in a stack is
not the order they are *explored*.

Marking on pop records a node only when the search actually arrives there. The
cost is that a node can sit on the stack more than once before it is reached.
`if visited[node]: continue` throws away the stale copies.

### Why `reversed`

A stack pops the last thing pushed. Pushing `adj[0] = [1, 2]` in order means `2`
comes out first. Reversing the push puts `1` on top, so the search follows
neighbours in list order, the same order a recursive DFS would.

Both are valid DFS orders. Without `reversed` this graph gives
`[0, 2, 4, 5, 3, 1]`; with it, `[0, 1, 3, 5, 4, 2]`.

### Trace

```
stack        pop   skip?   push (reversed)   ans
[0]          0             2, 1              [0]
[2, 1]       1             3                 [0, 1]
[2, 3]       3             5                 [0, 1, 3]
[2, 5]       5             4                 [0, 1, 3, 5]
[2, 4]       4             2                 [0, 1, 3, 5, 4]
[2, 2]       2                               [0, 1, 3, 5, 4, 2]
[2]          2     yes
[]           loop ends
```

`2` was pushed by `0` early on and again by `4`. The second copy is reached
first; the first copy is the stale one skipped at the end.

Output: `[0, 1, 3, 5, 4, 2]`.

## BFS vs DFS

| | BFS | DFS |
|---|---|---|
| Container | `Queue`, oldest first | `Stack`, newest first |
| Mark visited | on push | on pop |
| Explores | ring by ring, by distance | one path to the end, then backs up |
| Good for | shortest path (unweighted), levels | connectivity, cycles, paths, backtracking |
| Output here | `[0, 1, 2, 3, 4, 5]` | `[0, 1, 3, 5, 4, 2]` |

The two loops are almost identical. The container and where `visited` is set
are the whole difference.

## Cycle detection

```python
def dfs(i, parent, adj, visited):
    visited[i] = True

    for x in adj[i]:
        if x == parent:
            continue
        if visited[x]:
            return True
        if dfs(x, i, adj, visited):
            return True
    return False


def has_cycle(n, adj):
    visited = [False] * n
    for i in range(n):
        if not visited[i] and dfs(i, -1, adj, visited):
            return True
    return False
```

This is DFS written recursively. The call stack plays the role of `Stack`.

### The idea

In a tree there is exactly one path between any two nodes. So if DFS, walking
outward, finds a neighbour that is **already visited**, there must be a second
way to reach it. That second path closes a loop.

### Why `parent` is skipped

In an undirected graph every edge is stored both ways. Walk `0 -> 1`, and `0`
appears in `adj[1]`, already visited. That is not a second path, it is the same
edge seen from the other end. Without the skip, every graph with at least one
edge reports a cycle.

`parent` is the node this call was reached from, which is why the recursive
call passes `i`, the current node, as the child's parent:

```python
if dfs(x, i, adj, visited):        # right
if dfs(x, parent, adj, visited):   # WRONG
```

The wrong version keeps passing `-1` down. After the first level the skip never
matches, every child sees where it came from as visited, and the answer is
`True` for any graph, including a tree. On a graph that really has a cycle it
returns the right answer for the wrong reason, which is how the bug hid at
first.

### Why loop over every node

`dfs(0, ...)` only explores the part of the graph reachable from `0`. If the
graph is in several disconnected pieces, a cycle in another piece is never
seen. `has_cycle` starts a fresh DFS from each node that is still unvisited,
which covers every piece. `visited` is shared across those calls, so each node
is still explored once overall.

### Trace

`cycle.py` checks two graphs, the same six nodes with and without `[4, 5]`:

```
tree                     cyclic
    0                        0
   / \                      / \
  1   2                    1   2
  |   |                    |   |
  3   4                    3   4
  |                         \ /
  5                          5
```

On `cyclic`, DFS goes `0 -> 1 -> 3 -> 5`. At `5`, the neighbours are `3` (the
parent, skipped) and `4` (unvisited, recurse). At `4`, the neighbours are `2`
(unvisited, recurse) and `5` (the parent, skipped). At `2`, the neighbours are
`0` and `4`. `4` is the parent. `0` is visited and is **not** the parent, so
there is a cycle.

On `tree`, every visited neighbour that DFS meets is the node it just came
from. `has_cycle` returns `False`.

Output:

```
tree:   False
cyclic: True
```

### Directed graphs need something else

This method is for undirected graphs only. In a directed graph, reaching a
visited node does not mean a cycle: `0 -> 1`, `0 -> 2`, `2 -> 1` reaches `1`
twice with no loop. Directed cycle detection tracks which nodes are on the
**current** recursion path, not just which were ever visited (LeetCode 207).

## Bugs hit while writing it

**Forgetting to queue the start node.** Marking `0` visited and adding it to
`ans` is not enough. If `q` is empty, `while len(q) > 0` is false immediately
and the search never runs. Output is `[0]` with no error.

**Reusing `visited` and `ans` across searches.** After BFS every node is
visited, so DFS skips everything and only appends to BFS's old list. Output was
`[0, 1, 2, 3, 4, 5, 0]`. Fixed by creating both inside each function.

**Pushing the DFS start node onto the queue instead of the stack.** Same
symptom as forgetting to queue it: empty container, loop never runs.

**Marking DFS nodes visited on push.** Gave `[0, 1, 2, 4, 5, 3]`, which is a
BFS-looking prefix followed by a dive. See above.

**`q.pop()` instead of `q.popleft()`.** `deque.pop()` removes from the right,
the end you just appended to. That is last in, first out, which is a stack.
The code still runs and still visits every node, just in a depth-first-ish
order instead of by distance. No error, wrong answer.

**`q.push(x)`.** `deque` has no `push`. It is `append`. This one at least
crashes with `AttributeError`.

**Passing `parent` instead of `i` in cycle detection.** Reported a cycle in a
tree. See the cycle detection section.

The last two came from using `deque` directly. `graph.py` now uses `Queue`,
whose `push` and `pop` always mean the right thing. See
`stack_queue/stack_queue.md` for why `deque` is underneath it.

## Complexity

`V` is the number of nodes, `E` the number of edges.

| | Time | Space |
|---|---|---|
| Building `adj` | O(V + E) | O(V + E) |
| BFS | O(V + E) | O(V) for `visited` and the queue |
| DFS | O(V + E) | O(V + E) worst case, since a node can be pushed once per edge |
| `has_cycle` | O(V + E) | O(V) for `visited` and the recursion depth |
| Adjacency matrix | O(V²) to build | O(V²) |

BFS is O(V + E) because each node is popped once and, when it is, its
neighbour list is scanned once. Across the whole run that scans every edge
twice in an undirected graph (once from each end), which is still O(E).

## Quick rules

- Convert the edge list to an adjacency list before doing anything else.
- Undirected means append both ways. Directed means one way.
- `[[] for _ in range(n)]`, never `[[]] * n`.
- Graphs have cycles, so every traversal needs `visited`.
- BFS: mark visited when a node enters the queue.
- DFS: mark visited when a node leaves the stack, and skip repeats.
- Put the start node in the container before the loop.
- Give each search its own `visited` and `ans`.
- `append` + `popleft` is a queue. `append` + `pop` is a stack.
- BFS on an unweighted graph finds shortest paths by edge count.
- Undirected cycle: a visited neighbour that is not the parent.
- Pass the current node as the child's parent, not the parent you received.
- Loop over every node so disconnected pieces are checked too.

## Problems

- LeetCode 1971, Find if Path Exists in Graph
- LeetCode 547, Number of Provinces
- LeetCode 200, Number of Islands (grid as an implicit graph)
- LeetCode 994, Rotting Oranges (multi-source BFS)
- LeetCode 133, Clone Graph
- LeetCode 785, Is Graph Bipartite?
- LeetCode 684, Redundant Connection (the edge that creates a cycle)
- LeetCode 261, Graph Valid Tree (connected and no cycle)
- LeetCode 207, Course Schedule (DFS cycle detection, directed graph)
- LeetCode 797, All Paths From Source to Target (DFS)
