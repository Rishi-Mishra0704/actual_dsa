# Searching

Linear search, binary search, and peak finding.

## Linear search

Scan every element until you hit the target. O(n) time, O(1) space.

Works on anything. No precondition. This is the fallback whenever the input is
unsorted and there is no exploitable structure.

## Binary search

O(log n) time, O(1) space. Requires sorted input.

Look at the middle element. One comparison tells you which half cannot contain
the target, so you discard it. Repeat on what remains.

```
left, right = 0, len(nums) - 1
while left <= right:
    mid = (left + right) // 2
    if nums[mid] == target:  return mid
    elif nums[mid] < target: left = mid + 1
    else:                    right = mid - 1
return -1
```

Eleven elements takes four comparisons. Twenty two takes five. Doubling the
input costs exactly one more step, which is what log n means.

### Why the +1 and -1

You already checked `mid` and it was not the target. Excluding it is what makes
the window strictly smaller each iteration. Without it, a two element window
can pick the same mid forever and the loop never terminates.

## Peak finding

O(log n) time. Does **not** require sorted input, which is the interesting part.

A peak is strictly greater than both neighbours, with `nums[-1]` and `nums[n]`
treated as negative infinity.

```
left, right = 0, len(nums) - 1
while left < right:
    mid = (left + right) // 2
    if nums[mid] < nums[mid + 1]: left = mid + 1
    else:                         right = mid
return left
```

### Why one comparison is enough

A peak needs both neighbours checked, but the algorithm only checks the right
one. The left check comes free from how the pointer got there.

Two properties hold at all times:

- `nums[left]` is greater than its left neighbour
- `nums[right]` is greater than its right neighbour

Both are true initially because of the negative infinity boundaries. Every move
preserves them:

- `nums[mid] < nums[mid+1]`, set `left = mid + 1`. You just proved the new left
  beats its left neighbour.
- `nums[mid] > nums[mid+1]`, set `right = mid`. You just proved the new right
  beats its right neighbour.

When they converge on one index, both properties apply to that element at once.
Peak, never explicitly verified.

### Why the slope argument works

If you are on an ascending slope, going right either keeps rising until the
array ends (the last element is a peak, since the boundary is negative infinity)
or it turns downward somewhere (the turn is a peak). A peak on that side is
guaranteed either way. Same reasoning mirrored for descending.

## The two loop templates

These are different and mixing them up is the most common binary search bug.

**Exact match. `while left <= right`, `right = mid - 1`.**
Searching for a specific value. Returns -1 when absent. The window can legally
become empty.

**Convergence. `while left < right`, `right = mid`.**
Narrowing to a position that always exists. Peak finding, rotated array minimum,
"smallest value satisfying X". Never returns empty, so the answer is `left` when
the loop exits.

Using `right = mid` with `<=` gives an infinite loop. Using `right = mid - 1`
in a convergence problem skips the answer when mid is it.

## Common bugs

**Index versus value.** `left`, `right`, `mid` are positions. `nums[left]`,
`nums[mid]` are contents. Comparisons against a target always need the
`nums[...]` wrapper. `nums[mid] < left` is comparing a value to an index and
will silently return wrong answers rather than crashing.

**`right = len(nums) - 1`, not `nums[-1]`.** The last index, not the last value.

**Return the index, not the element.** `return mid`, not `return nums[mid]`.
The caller already knows the value, they asked where it is.

**Overflow.** `(left + right) // 2` is safe in Python because ints are
arbitrary precision. In Go, Java, or C it can overflow on large arrays. Use
`left + (right - left) // 2` there.

**Sorted precondition.** Standard binary search on unsorted input returns
garbage, not an error. Check the constraint before reaching for it.

## Choosing an approach

The question is what a single comparison buys you.

**Binary search** when one look at `mid` lets you discard half the remaining
search space. Signals:

- The problem states O(log n)
- Input is sorted, or rotated-sorted
- There is a monotonic predicate: false, false, false, true, true. Find the
  boundary.
- "Minimum value that satisfies X" or "maximum value that still works". This is
  binary search on the answer, not on the array.
- A local property plus guaranteed boundaries, like peak finding

Sorting is not the requirement. Eliminating half is.

**Two pointers** when comparing the elements at two positions tells you which
pointer to move. O(n). Signals:

- Sorted array, find a pair summing to a target
- Palindrome check, reverse in place, partition
- Container with most water, trapping rain water
- Two sequences merged or compared in one pass

**Sliding window**, a two pointer variant, when the answer is a contiguous
subarray or substring meeting a constraint. Both pointers move forward only.

**Fast and slow pointers** for cycle detection, finding the middle of a linked
list, or kth from the end.

### The discriminator

Binary search **discards** half the space per step, giving log n. Two pointers
**advances** one position per step, giving n.

If the problem allows O(n), two pointers is usually simpler and less bug prone.
If it demands O(log n), two pointers cannot get there and binary search is the
only realistic option. Read the required complexity first, it often names the
technique outright.

## Complexity

| Algorithm | Time | Space | Precondition |
|---|---|---|---|
| Linear search | O(n) | O(1) | none |
| Binary search | O(log n) | O(1) | sorted |
| Peak finding | O(log n) | O(1) | none |

## Problems

- LeetCode 704, Binary Search
- LeetCode 162, Find Peak Element
- LeetCode 33, Search in Rotated Sorted Array
- LeetCode 153, Find Minimum in Rotated Sorted Array
- LeetCode 875, Koko Eating Bananas (binary search on the answer)
- LeetCode 4, Median of Two Sorted Arrays (hard, revisit later)