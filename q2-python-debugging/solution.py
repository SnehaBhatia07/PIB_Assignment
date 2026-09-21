def find_duplicates(items):
    seen = set()
    duplicates = set()

    for item in items:
        if item in seen:
            duplicates.add(item)
        else:
            seen.add(item)

    result = []
    added = set()
    for item in items:
        if item in duplicates and item not in added:
            result.append(item)
            added.add(item)

    return result


def buggy_find_duplicates(items):
    """Original buggy implementation from assessment specification."""
    duplicates = []
    for item in items:
        if items.count(item) > 1:
            duplicates.append(item)
    return duplicates


if __name__ == "__main__":
    example = [1, 2, 3, 2, 4, 1, 5, 2]
    print("--- Question 2: Duplicate Detection ---")
    print(f"Input List       : {example}")
    print(f"Buggy Output     : {buggy_find_duplicates(example)} (Incorrect repetition, O(N^2))")
    print(f"Optimized Output : {find_duplicates(example)} (Correct expected result, O(N))")
