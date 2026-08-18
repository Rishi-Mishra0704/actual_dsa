# Recursion Notes

## What recursion actually does
- Every recursive function call creates a new **stack frame** on the Call Stack.
- Each stack frame stores:
  - Local variables
  - Function parameters
  - Return address (where execution resumes after the recursive call returns)

Example:

```python
def print1toN(n):
    if n < 1:
        return
    print1toN(n - 1)
    print(n)
```

Call order:
100 → 99 → 98 → ... → 1 → 0

Return order:
0 → 1 → 2 → ... → 99 → 100

Output:
1 2 3 ... 100

Reason:
- Code BEFORE the recursive call executes while going DOWN.
- Code AFTER the recursive call executes while the stack UNWINDS.

General Rule:
func()
├── code before recursion   <-- executes first
├── recursive call
└── code after recursion    <-- executes after child returns

## Call Stack (LIFO)
Stack = Last In, First Out.

Example:

push(3)
push(2)
push(1)
push(0)

pop(0)
pop(1)
pop(2)
pop(3)

The most recent recursive call always finishes first.

## Base Case
Every recursive function MUST have a base case.

Without one:

```python
def f(n):
    f(n-1)
```

Result:
RecursionError: maximum recursion depth exceeded

## Python Recursion Limit
Python limits recursion depth to roughly 1000 calls by default.

Check:

```python
import sys
print(sys.getrecursionlimit())
```

Change (only when necessary):

```python
sys.setrecursionlimit(2000)
```

Increasing it too much can crash the interpreter due to stack overflow.

## Time Complexity
Recursion itself is NOT slow.

A recursive function with one recursive call per level:

O(n)

Example:
print1toN()

100 recursive calls is extremely fast.

The expensive part is:
- Too many recursive calls
- Recomputing the same work

## Memoization
Memoization stores previously computed answers.

Without memoization:

fib(5)
├── fib(4)
│   ├── fib(3)
│   └── fib(2)
└── fib(3)

fib(3) is computed multiple times.

With memoization:
Each state is computed only once.

Memoization reduces TIME.

It DOES NOT reduce recursion depth.

## When to use recursion
Good:
- Trees
- Graph DFS
- Divide & Conquer
- Backtracking
- Dynamic Programming (top-down)

Avoid:
- Simple counting
- Iterating arrays
- Large linear recursion (>1000 depth in Python)

Use loops instead.

## Recursion Mental Model

Going down:
Push stack frames.

Coming back:
Pop stack frames.

Anything after the recursive call executes while popping.

## Interview Tip
Always ask:
1. What is the base case?
2. What is the recursive relation?
3. What is the recursion depth?
4. Is there overlapping work? (Memoization)
5. Can this be converted to iteration?

## Quick Rules
- Every recursive call creates a new stack frame.
- Call Stack is LIFO.
- Base case stops recursion.
- Before recursion = executed while going down.
- After recursion = executed while coming back.
- Python recursion limit ≈ 1000.
- Memoization saves repeated work, NOT stack depth.
- Loops are preferred for simple linear iteration.
- Recursion is preferred when the problem is naturally recursive.