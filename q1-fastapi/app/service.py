from app.schemas import TransactionCreate, TransactionSummary

transactions: list[dict] = []


def create_transaction(data: TransactionCreate) -> dict:
    record = data.model_dump()
    transactions.append(record)
    return record


def get_transactions(user_id: str) -> list[dict]:
    return [t for t in transactions if t["user_id"] == user_id]


def get_user_summary(user_id: str) -> TransactionSummary:
    user_txs = get_transactions(user_id)
    total_credit = sum(t["amount"] for t in user_txs if t["type"] == "credit")
    total_debit = sum(t["amount"] for t in user_txs if t["type"] == "debit")
    balance = total_credit - total_debit

    return TransactionSummary(
        total_credit=round(total_credit, 2),
        total_debit=round(total_debit, 2),
        balance=round(balance, 2),
    )


def clear_storage() -> None:
    transactions.clear()
