# Stacks and Queues

`Stack` and `Queue`, both with `push`, `pop`, a peek (`top` / `front`), and
`size`. Used by `graph/` for DFS and BFS.

## The one difference

Both containers hold items and hand them back. The only question is **which
one comes out next**.

```
push 1, 2, 3

Stack   pop -> 3, 2, 1     last in, first out   (LIFO)
Queue   pop -> 1, 2, 3     first in, first out  (FIFO)
```

A stack is a pile of plates: you take from the top, which is whatever you put
down last. A queue is a line at a counter: whoever arrived first is served
first.

Everything else follows from that. DFS uses a stack because it wants to keep
following the node it just found. BFS uses a queue because it wants to finish
older nodes before newer ones.

## Stack

```python
class Stack:
    def __init__(self):
        self.stack = []

    def push(self, x):
        self.stack.append(x)

    def pop(self):
        if len(self.stack) == 0:
            return -1
        return self.stack.pop()

    def top(self):
        if len(self.stack) == 0:
            return -1
        return self.stack[-1]

    def size(self):
        return len(self.stack)
```

A Python list is already a good stack. `append` and `pop()` both work at the
**end** of the list, where nothing needs shifting, so both are O(1).

The top of the stack is `self.stack[-1]`. `top()` looks at it, `pop()` removes
it.

## Queue

```python
from collections import deque

class Queue:
    def __init__(self):
        self.queue = deque()

    def push(self, x):
        self.queue.append(x)

    def pop(self):
        if len(self.queue) == 0:
            return -1
        return self.queue.popleft()

    def front(self):
        if len(self.queue) == 0:
            return -1
        return self.queue[0]

    def size(self):
        return len(self.queue)
```

Items go in at the back (`append`) and come out at the front (`popleft`).

### Why `deque` and not a list

A list could do it with `append` and `pop(0)`, but `pop(0)` removes the
**first** element, and every element after it shifts down one slot. That is
O(n) per pop, so draining a queue of n items costs O(n²).

`deque` is a double ended queue, built to add and remove at both ends in O(1).

| | end (right) | front (left) |
|---|---|---|
| list | `append`, `pop()` O(1) | `insert(0, x)`, `pop(0)` **O(n)** |
| deque | `append`, `pop()` O(1) | `appendleft`, `popleft()` O(1) |

### `deque.pop()` is not a queue pop

`deque` has both `pop()` and `popleft()`. `pop()` takes from the right, the
same end `append` adds to, which makes it a stack. Using it in BFS gives no
error, just the wrong order. `Queue.pop()` hides this by always calling
`popleft()`.

## Empty behaviour

`pop`, `top`, and `front` return `-1` on an empty container instead of raising.
That is convenient for small exercises, but it means `-1` cannot be stored as a
real value: you could not tell "popped -1" from "was empty". Check `size()`
first in loops:

```python
while stack.size() > 0:
    node = stack.pop()
```

Raising `IndexError` instead, like `list.pop()` does, is the stricter choice.

## The file name `queue.py`

Python's standard library also has a module called `queue`. Inside the package
it is safe: `from stack_queue.queue import Queue` is unambiguous. But running a
script from **inside** `stack_queue/` puts that folder first on the import path,
and any `import queue` there, including ones inside library code, picks up this
file instead of the standard one. Run things from the project root with
`python -m`.

## Complexity

| Operation | Stack | Queue |
|---|---|---|
| `push` | O(1) | O(1) |
| `pop` | O(1) | O(1) |
| `top` / `front` | O(1) | O(1) |
| `size` | O(1) | O(1) |

## Quick rules

- Stack is LIFO, queue is FIFO.
- A list is a fine stack. A list is a bad queue; use `deque`.
- `popleft()` for a queue, `pop()` for a stack.
- With `-1` as the empty signal, loop on `size() > 0`, not on the popped value.
- DFS uses a stack, BFS uses a queue.

## Problems

- LeetCode 20, Valid Parentheses (stack)
- LeetCode 155, Min Stack
- LeetCode 232, Implement Queue using Stacks
- LeetCode 225, Implement Stack using Queues
- LeetCode 739, Daily Temperatures (monotonic stack)
- LeetCode 933, Number of Recent Calls (queue)
