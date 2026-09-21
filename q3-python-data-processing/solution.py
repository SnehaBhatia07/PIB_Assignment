import json
from pathlib import Path


def load_data(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def process_users(users):
    # Step 1: Remove duplicate user_id records, retaining the first occurrence
    seen_ids = set()
    deduped_users = []
    for user in users:
        user_id = user["user_id"]
        if user_id not in seen_ids:
            seen_ids.add(user_id)
            deduped_users.append(user)

    # Step 2: Remove records where score < 50
    filtered_users = [user for user in deduped_users if user["score"] >= 50]

    # Handle edge case: empty dataset or no valid users
    if not filtered_users:
        return {
            "users": [],
            "average_score": 0,
            "max_score": 0,
            "min_score": 0,
            "top_10": [],
        }

    # Step 3: Calculate score statistics
    scores = [user["score"] for user in filtered_users]
    average_score = round(sum(scores) / len(scores), 2)
    max_score = max(scores)
    min_score = min(scores)

    # Step 4: Determine top 10 users by score descending (stable sort preserves order on ties)
    top_10 = sorted(filtered_users, key=lambda user: user["score"], reverse=True)[:10]

    return {
        "users": filtered_users,
        "average_score": average_score,
        "max_score": max_score,
        "min_score": min_score,
        "top_10": top_10,
    }


if __name__ == "__main__":
    current_dir = Path(__file__).parent
    data_path = current_dir / "data.json"
    users_data = load_data(data_path)
    results = process_users(users_data)

    print("Data Processing Results:")
    print(f"Total Valid Users : {len(results['users'])}")
    print(f"Average Score     : {results['average_score']}")
    print(f"Maximum Score     : {results['max_score']}")
    print(f"Minimum Score     : {results['min_score']}")
    print(f"Top Users Count   : {len(results['top_10'])}")
    print("\nTop 10 Users:")
    for idx, user in enumerate(results["top_10"], 1):
        print(f"  {idx:2d}. {user['name']} (ID: {user['user_id']}) - Score: {user['score']}")
