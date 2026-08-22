# Linked Lists

Singly linked list: append, count, print, insert_at, remove_at, reverse.

## Structure

```python
class Node:
    def __init__(self, val=0, nextNode=None):
        self.val = val
        self.next = nextNode
```

A node holds a value and a reference to the next node. The list itself owns
exactly one thing, `self.head`. Everything else is reached by walking.

There is no index, no length field, no contiguous block of memory. Nodes sit
wherever the allocator put them. The only thing making them a list is the chain
of `next` references, and the only entry point into that chain is `head`.

Two consequences follow from that and they explain most of the complexity table
at the bottom:

- To reach position `k` you must walk `k` links. There is no arithmetic
  shortcut, so random access is O(n).
- Once you are holding the node before a position, inserting or removing there
  is O(1). No shifting, just pointer reassignment.

`head is None` means empty. The last node's `next` is `None`.

## Dangling nodes

This is the part that breaks lists, so it comes before the methods.

**A node is part of the list only when it is reachable from `head`.** Creating
it is not enough. `Node(value)` allocates an object floating in memory with no
relationship to your list whatsoever.

```python
new_node = Node(value)   # exists, but is NOT in the list
```

At this moment `new_node` is **dangling**. `count()` will not see it. `print()`
will not see it. It becomes part of the list at exactly one instant: when some
node already in the chain, or `head` itself, is made to point at it.

```python
current.next = new_node   # NOW it is in the list
```

So every insertion has two phases, and the list is in a torn state between them:

1. The new node is dangling. It exists but is invisible to every traversal.
2. Someone in the list points at it. Now it is a member.

### The rule this forces

**Wire the dangling node's outgoing pointer first. Rewire the list's pointer
into it second.**

Look at `insert_at`:

```python
new_node.next = current.next   # 1. dangling node points INTO the list
current.next = new_node        # 2. list now points AT the dangling node
```

Starting from `A -> B -> C` and inserting `N` after `A`:

```
step 0    A -> B -> C          N            (N dangling, points to None)

step 1    A -> B -> C          N ---^       (N.next = A.next, so N -> B)
              ^________________|            A still points to B

step 2    A -> N -> B -> C                  (A.next = N, N joins the chain)
```

After step 1 two nodes point at `B`. That is fine and temporary. `B` does not
care how many references point at it, and a traversal from `head` still gives
`A -> B -> C`, an intact list.

Now swap the two lines:

```python
current.next = new_node        # WRONG order
new_node.next = current.next
```

```
step 1    A -> N               B -> C       (A.next = N; nothing points to B)

step 2    A -> N               B -> C       (N.next = A.next, which is now N)
               ^__|                          N points to itself
```

The moment `A.next = N` executes, the only reference to `B` is destroyed. `B`
and `C` are unreachable and gone. Then line 2 reads `current.next`, which now
returns `N` itself, and you get a self-referencing node. `print()` loops
forever.

The reason for the ordering is simple: `current.next` is the only surviving
reference to the rest of the list. You must copy it somewhere safe before you
overwrite it. Step 1 copies it into `new_node.next`. That is the whole trick.

### Never operate on a list that has a dangling node in flight

Between the two lines, the list is mid-surgery. Do not call `count()`,
`print()`, another `insert_at`, or anything else in that gap, and do not
`return` early from it. A traversal at that point either misses the new node or
walks a chain that is only half-rewired. Finish the wiring, then operate.

The same applies at the head:

```python
new_node.next = self.head   # dangling node points at the old first node
self.head = new_node        # head moves; the node is now the list's front
```

Reversed, `self.head = new_node` drops the reference to the old first node and
the entire list is lost in one assignment.

### The mirror case: orphaned nodes on removal

Removal produces the opposite situation. In `remove_at`:

```python
current.next = current.next.next
```

The removed node is now unreachable from `head`, so it is out of the list. But
**it still points at its old successor.** It is an orphan holding a stale
reference into a list it no longer belongs to.

```
before    A -> B -> C          remove B
after     A ------> C
               B ---^          B is out, but B.next is still C
```

If you kept a variable pointing at that node, do not trust its `next`. Reading
it walks back into the live list from a node that is not in it, and writing
through it can corrupt the list. In Python the orphan is garbage collected once
nothing references it, so normally it just disappears. It only bites when you
saved it first.

### The mental checklist

Before any pointer assignment, ask:

1. Is the node I am about to overwrite the *only* path to the rest of the list?
2. If yes, have I already saved that path somewhere?

`insert_at` saves it in `new_node.next`. `reverse` saves it in `next_node`.
Every correct pointer manipulation is doing one or the other.

## append

```python
def append(self, val):
    new_node = Node(val)
    if self.head is None:
        self.head = new_node
        return
    current = self.head
    while current.next:
        current = current.next
    current.next = new_node
```

Empty list is a special case because there is no node to attach to; the only
pointer that can be modified is `head` itself.

Otherwise walk to the last node. The loop condition is `current.next`, not
`current`. That difference matters: `while current` walks until `current` is
`None`, which lands you past the end holding nothing. `while current.next`
stops **on** the last node, which is what you need, because you cannot attach
to `None`.

O(n), because there is no tail pointer. Keeping one would make this O(1).

## count and print

Both are plain traversals with `while current`, since they visit every node
including the last and stop when they fall off the end.

```python
current = self.head
while current:
    ...
    current = current.next
```

O(n). There is no stored length, so `count()` genuinely walks the list every
time. Do not call it inside a loop.

## insert_at

```python
def insert_at(self, index, value):
    new_node = Node(value)

    if index == 0:
        new_node.next = self.head
        self.head = new_node
        return

    current = self.head
    for _ in range(index - 1):
        if current is None:
            raise IndexError('index out of range')
        current = current.next
    new_node.next = current.next
    current.next = new_node
```

To insert at `index`, you need the node at `index - 1`, because a singly linked
node cannot reach backwards. That is why the loop runs `index - 1` times and
why `index == 0` needs its own branch: position 0 has no predecessor, so `head`
is the pointer that must change.

For `index = 1` the loop body never runs and `current` stays at `head`, which is
correct: `head` is the node before position 1.

Pointer work is the two lines analysed above, in that order.

O(n) to walk, O(1) to splice.

## remove_at

```python
def remove_at(self, index):
    if self.head is None:
        raise IndexError("cannot delete from empty list")

    if index == 0:
        self.head = self.head.next
        return

    current = self.head
    for _ in range(index - 1):
        if current is None:
            raise IndexError("index out of bound")
        current = current.next

    if current is None or current.next is None:
        raise IndexError("index out of bound")

    current.next = current.next.next
```

Same predecessor requirement. Removing at 0 just moves `head` forward; the old
first node is orphaned and collected.

The post-loop guard is doing real work and is worth keeping. Two distinct
failures:

- `current is None` — the walk ran off the end, so the predecessor does not
  exist.
- `current.next is None` — the predecessor is the last node, so there is
  nothing after it to remove.

Without that check, `current.next.next` raises `AttributeError` on `None`
instead of a meaningful `IndexError`.

Note `remove_at` never allocates. Nothing dangling is created; the concern here
is the orphan, described above.

## reverse

```python
def reverse(self):
    prev = None
    current = self.head
    while current is not None:
        next_node = current.next
        current.next = prev
        prev = current
        current = next_node
    return prev
```

Three pointers, and the order of the four lines is not negotiable.

`current.next = prev` destroys the forward link. Once it executes, the rest of
the list is unreachable from `current`. So `next_node = current.next` has to
come first — it is the saved path from the checklist above.

Then `prev` and `current` both step forward. `prev` trails one behind, and it
is the head of the growing reversed section.

```
start     None   1 -> 2 -> 3 -> None
                 ^
                 current, prev = None

after 1   None <- 1    2 -> 3 -> None
                  ^    ^
                  prev current

after 2   None <- 1 <- 2    3 -> None
                       ^    ^
                       prev current

after 3   None <- 1 <- 2 <- 3    None
                            ^    ^
                            prev current

loop ends when current is None; prev is the new head
```

**Mid-loop the list is genuinely split in two**, a reversed front half hanging
off `prev` and an untouched back half hanging off `current`, with no link
between them. `self.head` is still pointing at the original first node, which by
now is the *tail* of the reversed portion and points at `None`. Calling
`print()` or `count()` at that moment reports a list of length 1. The list is
only whole again when the loop finishes.

### The return value is a trap

`reverse` returns the new head instead of assigning it, so the caller must
write it back:

```python
ll.head = ll.reverse()
```

Forget the assignment and `head` still refers to the old first node. That node
is now the last node with `next = None`, so the list silently looks like it has
one element. Nothing raises. Every node is still there, just unreachable.

Assigning `self.head = prev` inside the method and returning nothing would
remove the footgun.

## Rough edges in the current code

Real bugs in this implementation, worth fixing when you revisit it.

**`insert_at` can raise `AttributeError` instead of `IndexError`.** The `None`
check sits at the top of the loop body, so it never inspects `current` after
the final advance. On a 3-element list, `insert_at(4, x)` leaves `current` as
`None` when the loop exits, and `new_node.next = current.next` crashes with
`AttributeError: 'NoneType' object has no attribute 'next'`. Same on an empty
list with any non-zero index. `remove_at` has the guard that fixes this;
`insert_at` needs the same one after its loop.

**Negative indices are accepted silently.** `range(index - 1)` with a negative
`index` is empty, so `insert_at(-5, x)` inserts at position 1 and
`remove_at(-5)` removes it. Should raise.

**`print` shadows the builtin** inside the class body. It works here because the
call inside the method resolves to the global builtin, not the method, but it
is a name worth avoiding. `display` or `__str__` is safer.

**`ReverseLinkedList.__init__` re-declares `self.head = None`** instead of
calling `super().__init__()`. Harmless now, but it diverges the moment the base
class initialises anything else.

## Complexity

| Operation | Time | Note |
|---|---|---|
| `append` | O(n) | O(1) with a tail pointer |
| `count` | O(n) | no stored length |
| `print` | O(n) | |
| `insert_at(0)` | O(1) | no walk needed |
| `insert_at(k)` | O(n) | O(n) walk, O(1) splice |
| `remove_at(0)` | O(1) | |
| `remove_at(k)` | O(n) | |
| `reverse` | O(n) time, O(1) space | iterative, in place |
| access by index | O(n) | the defining weakness |

Space is O(n) for the list, plus O(1) per operation. `reverse` allocates
nothing.

## Linked list vs array

Arrays win on access and on cache locality, which matters more in practice than
the table suggests. Contiguous memory means the CPU prefetches the next elements
for free; linked list nodes are scattered, so each hop can be a cache miss.

Linked lists win when you are inserting or removing at a position you already
hold a reference to, especially at the front. `insert_at(0)` is O(1) here and
O(n) on an array, which shifts every element.

Reach for a linked list when the problem is about splicing, and for an array
when it is about indexing.

## Quick rules

- A node is in the list only when reachable from `head`. Allocation is not
  membership.
- A freshly created node is dangling. Connect it before doing anything else.
- Point the dangling node into the list first, then point the list at it.
- Never overwrite a `next` that is the only path to the remainder without
  saving it first.
- Never traverse a list that is mid-rewire.
- A removed node keeps a stale `next` into the live list. Do not follow it.
- Singly linked nodes cannot look backwards, so mutation always needs the
  *predecessor*.
- `while current` traverses to the end. `while current.next` stops on the last
  node. Use the second when you need to attach something.
- Position 0 always needs its own branch, because `head` is the pointer being
  modified.
- If a method returns a new head, assign it.

## Problems

- LeetCode 206, Reverse Linked List
- LeetCode 21, Merge Two Sorted Lists
- LeetCode 141, Linked List Cycle (fast and slow pointers)
- LeetCode 876, Middle of the Linked List
- LeetCode 19, Remove Nth Node From End (two pointers, one gap apart)
- LeetCode 2, Add Two Numbers
- LeetCode 143, Reorder List (combines middle, reverse, and merge)
