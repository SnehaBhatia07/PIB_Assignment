import json
import sys
from pathlib import Path
try:
    import pytest
except ImportError:
    pytest = None

# Ensure local solution is loaded
sys.path.insert(0, str(Path(__file__).parent))

from solution import load_data, process_users


def test_normal_dataset():
    data = [
        {"user_id": "1", "name": "Alice", "age": 20, "score": 80},
        {"user_id": "2", "name": "Bob", "age": 22, "score": 70},
        {"user_id": "3", "name": "Charlie", "age": 21, "score": 90},
    ]
    result = process_users(data)
    assert len(result["users"]) == 3
    assert result["average_score"] == 80.0
    assert result["max_score"] == 90
    assert result["min_score"] == 70
    assert len(result["top_10"]) == 3
    assert [u["score"] for u in result["top_10"]] == [90, 80, 70]


def test_duplicate_user_ids():
    data = [
        {"user_id": "101", "name": "Original", "age": 20, "score": 75},
        {"user_id": "101", "name": "Duplicate", "age": 20, "score": 95},
        {"user_id": "102", "name": "Other", "age": 21, "score": 80},
    ]
    result = process_users(data)
    assert len(result["users"]) == 2
    user_ids = [u["user_id"] for u in result["users"]]
    assert user_ids == ["101", "102"]


def test_first_duplicate_record_retained():
    data = [
        {"user_id": "101", "name": "FirstRecord", "age": 25, "score": 60},
        {"user_id": "101", "name": "SecondRecord", "age": 25, "score": 95},
    ]
    result = process_users(data)
    assert len(result["users"]) == 1
    assert result["users"][0]["name"] == "FirstRecord"
    assert result["users"][0]["score"] == 60


def test_users_with_score_below_50():
    data = [
        {"user_id": "1", "name": "Low1", "age": 20, "score": 49},
        {"user_id": "2", "name": "Low2", "age": 21, "score": 10},
        {"user_id": "3", "name": "Pass", "age": 22, "score": 65},
    ]
    result = process_users(data)
    assert len(result["users"]) == 1
    assert result["users"][0]["name"] == "Pass"
    assert result["min_score"] == 65


def test_score_exactly_50():
    data = [
        {"user_id": "1", "name": "Boundary", "age": 20, "score": 50},
        {"user_id": "2", "name": "Pass", "age": 21, "score": 70},
    ]
    result = process_users(data)
    assert len(result["users"]) == 2
    assert any(u["score"] == 50 for u in result["users"])
    assert result["min_score"] == 50


def test_average_score_rounding():
    data = [
        {"user_id": "1", "name": "U1", "age": 20, "score": 50},
        {"user_id": "2", "name": "U2", "age": 21, "score": 55},
        {"user_id": "3", "name": "U3", "age": 22, "score": 62},
    ]
    # (50 + 55 + 62) / 3 = 167 / 3 = 55.666... -> 55.67
    result = process_users(data)
    assert result["average_score"] == 55.67


def test_maximum_and_minimum_score():
    data = [
        {"user_id": "1", "name": "Min", "age": 20, "score": 55},
        {"user_id": "2", "name": "Mid", "age": 21, "score": 78},
        {"user_id": "3", "name": "Max", "age": 22, "score": 99},
    ]
    result = process_users(data)
    assert result["max_score"] == 99
    assert result["min_score"] == 55


def test_top_10_users_with_more_than_10_records():
    data = [
        {"user_id": str(i), "name": f"User_{i}", "age": 20 + i, "score": 50 + i * 2}
        for i in range(15)
    ]
    result = process_users(data)
    assert len(result["users"]) == 15
    assert len(result["top_10"]) == 10

    # Ensure top_10 is strictly sorted in descending score order
    top_scores = [u["score"] for u in result["top_10"]]
    assert top_scores == sorted(top_scores, reverse=True)
    assert top_scores[0] == 78  # max score 50 + 14 * 2 = 78
    assert top_scores[-1] == 60  # 10th score 50 + 5 * 2 = 60


def test_fewer_than_10_valid_users():
    data = [
        {"user_id": "1", "name": "A", "age": 20, "score": 85},
        {"user_id": "2", "name": "B", "age": 21, "score": 75},
        {"user_id": "3", "name": "C", "age": 22, "score": 65},
    ]
    result = process_users(data)
    assert len(result["top_10"]) == 3
    assert [u["score"] for u in result["top_10"]] == [85, 75, 65]


def test_empty_input():
    result = process_users([])
    assert result == {
        "users": [],
        "average_score": 0,
        "max_score": 0,
        "min_score": 0,
        "top_10": [],
    }


def test_all_users_filtered_out():
    data = [
        {"user_id": "1", "name": "Fail1", "age": 20, "score": 30},
        {"user_id": "2", "name": "Fail2", "age": 21, "score": 45},
        {"user_id": "3", "name": "Fail3", "age": 22, "score": 15},
    ]
    result = process_users(data)
    assert result == {
        "users": [],
        "average_score": 0,
        "max_score": 0,
        "min_score": 0,
        "top_10": [],
    }


def test_load_data(tmp_path):
    sample_file = tmp_path / "test_data.json"
    content = [{"user_id": "99", "name": "Test", "age": 25, "score": 88}]
    sample_file.write_text(json.dumps(content), encoding="utf-8")

    loaded = load_data(sample_file)
    assert loaded == content


if __name__ == "__main__":
    tests = [
        ("Normal Dataset & Sorting", test_normal_dataset),
        ("Duplicate user_id removal", test_duplicate_user_ids),
        ("First duplicate record retained", test_first_duplicate_record_retained),
        ("Filter scores below 50", test_users_with_score_below_50),
        ("Boundary score exactly 50 retained", test_score_exactly_50),
        ("Average score rounding to 2 decimals", test_average_score_rounding),
        ("Maximum and minimum score calculation", test_maximum_and_minimum_score),
        ("Top 10 users slice on > 10 records", test_top_10_users_with_more_than_10_records),
        ("Fewer than 10 valid users", test_fewer_than_10_valid_users),
        ("Empty input handling", test_empty_input),
        ("All users filtered out (< 50)", test_all_users_filtered_out),
    ]

    print("--- Running Q3 Unit Tests ---")
    for name, test_func in tests:
        test_func()
        print(f"  ✓ {name}")
    print("\nResult: All 11 unit tests passed successfully!")

