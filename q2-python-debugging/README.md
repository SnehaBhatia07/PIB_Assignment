# Q2: Python Duplicate Debugging

Optimization and debugging of `find_duplicates(items)`.

## Original Issues
1. `items.count(item) > 1` inside a loop results in an O(n^2) runtime.
2. Repeated duplicates are appended multiple times (`[1, 2, 2, 1, 2]` instead of `[1, 2]`).

## Solution
- Single-pass `seen` set combined with an `added` tracking set.
- Preserves the original first-appearance order.
- Time complexity: O(n).
- Space complexity: O(n).

## How to Test on Your Screen
Run from your terminal:
```bash
python3 -c "from solution import find_duplicates; print('Result:', find_duplicates([1, 2, 3, 2, 4, 1, 5, 2]))"
```
Output on screen: `Result: [1, 2]`

## Running Tests
```bash
pytest test_solution.py -v
```
All 6 tests pass.
