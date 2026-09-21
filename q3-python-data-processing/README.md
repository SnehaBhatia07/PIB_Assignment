# Q3: Python Data Processing

JSON data processing pipeline to deduplicate users, filter scores, calculate metrics, and return the top 10 users by score. Built purely with Python standard libraries.

## How to Test on Your Screen
Run the script directly from your terminal:
```bash
python3 solution.py
```
You will see the formatted results table printed directly on your screen:
```text
Data Processing Results:
Total Valid Users : 12
Average Score     : 78.5
Maximum Score     : 98
Minimum Score     : 50
Top Users Count   : 10
...
```

## Running Tests
```bash
pytest test_solution.py -v
```
All 12 tests pass.
