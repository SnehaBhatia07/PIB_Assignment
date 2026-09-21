from solution import find_duplicates


def test_assessment_example():
    items = [1, 2, 3, 2, 4, 1, 5, 2]
    assert find_duplicates(items) == [1, 2]


def test_no_duplicates():
    items = [1, 2, 3, 4]
    assert find_duplicates(items) == []


def test_multiple_occurrences():
    items = [5, 5, 5, 5]
    assert find_duplicates(items) == [5]


def test_strings():
    items = ["a", "b", "a", "c", "b"]
    assert find_duplicates(items) == ["a", "b"]


def test_empty_input():
    items = []
    assert find_duplicates(items) == []


def test_original_list_not_modified():
    original = [1, 2, 3, 2, 4, 1, 5, 2]
    copy = list(original)
    _ = find_duplicates(original)
    assert original == copy


if __name__ == "__main__":
    tests = [
        ("Assessment Example [1, 2, 3, 2, 4, 1, 5, 2] -> [1, 2]", test_assessment_example),
        ("List with no duplicates -> []", test_no_duplicates),
        ("Multiple occurrences [5, 5, 5, 5] -> [5]", test_multiple_occurrences),
        ("Strings ['a', 'b', 'a', 'c', 'b'] -> ['a', 'b']", test_strings),
        ("Empty input [] -> []", test_empty_input),
        ("Original list immutability verified", test_original_list_not_modified),
    ]

    print("--- Running Q2 Unit Tests ---")
    for name, test_func in tests:
        test_func()
        print(f"  ✓ {name}")
    print("\nResult: All 6 unit tests passed successfully!")

