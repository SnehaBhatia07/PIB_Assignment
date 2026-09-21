import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.service import clear_storage


@pytest.fixture(autouse=True)
def reset_in_memory_storage():
    clear_storage()
    yield
    clear_storage()


@pytest.fixture
def client():
    return TestClient(app)


def test_create_valid_credit_transaction(client):
    payload = {
        "user_id": "U1001",
        "amount": 1500,
        "type": "credit",
        "timestamp": "2026-09-18T10:30:00",
    }
    response = client.post("/transactions", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == "U1001"
    assert data["amount"] == 1500.0
    assert data["type"] == "credit"
    assert data["timestamp"] == "2026-09-18T10:30:00"


def test_create_valid_debit_transaction(client):
    payload = {
        "user_id": "U1001",
        "amount": 500,
        "type": "debit",
        "timestamp": "2026-09-18T11:00:00",
    }
    response = client.post("/transactions", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == "U1001"
    assert data["amount"] == 500.0
    assert data["type"] == "debit"
    assert data["timestamp"] == "2026-09-18T11:00:00"


def test_get_transactions_for_user(client):
    client.post(
        "/transactions",
        json={
            "user_id": "U1001",
            "amount": 1000,
            "type": "credit",
            "timestamp": "2026-09-18T10:00:00",
        },
    )
    client.post(
        "/transactions",
        json={
            "user_id": "U1001",
            "amount": 250,
            "type": "debit",
            "timestamp": "2026-09-18T10:30:00",
        },
    )

    response = client.get("/transactions/U1001")
    assert response.status_code == 200
    transactions = response.json()
    assert len(transactions) == 2
    assert transactions[0]["amount"] == 1000.0
    assert transactions[1]["amount"] == 250.0


def test_user_isolation(client):
    client.post(
        "/transactions",
        json={
            "user_id": "U1001",
            "amount": 1000,
            "type": "credit",
            "timestamp": "2026-09-18T10:00:00",
        },
    )
    client.post(
        "/transactions",
        json={
            "user_id": "U2002",
            "amount": 2000,
            "type": "credit",
            "timestamp": "2026-09-18T11:00:00",
        },
    )

    resp1 = client.get("/transactions/U1001")
    assert resp1.status_code == 200
    txs_user1 = resp1.json()
    assert len(txs_user1) == 1
    assert txs_user1[0]["user_id"] == "U1001"

    resp2 = client.get("/transactions/U2002")
    assert resp2.status_code == 200
    txs_user2 = resp2.json()
    assert len(txs_user2) == 1
    assert txs_user2[0]["user_id"] == "U2002"


def test_get_transactions_empty_user(client):
    response = client.get("/transactions/NON_EXISTENT_USER")
    assert response.status_code == 200
    assert response.json() == []


def test_summary_multiple_transactions(client):
    client.post(
        "/transactions",
        json={
            "user_id": "U1001",
            "amount": 5000,
            "type": "credit",
            "timestamp": "2026-09-18T10:00:00",
        },
    )
    client.post(
        "/transactions",
        json={
            "user_id": "U1001",
            "amount": 2500,
            "type": "debit",
            "timestamp": "2026-09-18T11:00:00",
        },
    )

    response = client.get("/transactions/U1001/summary")
    assert response.status_code == 200
    summary = response.json()
    assert summary["total_credit"] == 5000.0
    assert summary["total_debit"] == 2500.0
    assert summary["balance"] == 2500.0


def test_summary_empty_user(client):
    response = client.get("/transactions/NON_EXISTENT_USER/summary")
    assert response.status_code == 200
    summary = response.json()
    assert summary["total_credit"] == 0.0
    assert summary["total_debit"] == 0.0
    assert summary["balance"] == 0.0


def test_reject_negative_amount(client):
    payload = {
        "user_id": "U1001",
        "amount": -1500,
        "type": "credit",
        "timestamp": "2026-09-18T10:30:00",
    }
    response = client.post("/transactions", json=payload)
    assert response.status_code == 422


def test_reject_zero_amount(client):
    payload = {
        "user_id": "U1001",
        "amount": 0,
        "type": "credit",
        "timestamp": "2026-09-18T10:30:00",
    }
    response = client.post("/transactions", json=payload)
    assert response.status_code == 422


def test_reject_invalid_transaction_type(client):
    payload = {
        "user_id": "U1001",
        "amount": 100,
        "type": "transfer",
        "timestamp": "2026-09-18T10:30:00",
    }
    response = client.post("/transactions", json=payload)
    assert response.status_code == 422


def test_reject_invalid_timestamp(client):
    payload = {
        "user_id": "U1001",
        "amount": 100,
        "type": "credit",
        "timestamp": "not-a-valid-timestamp",
    }
    response = client.post("/transactions", json=payload)
    assert response.status_code == 422


def test_reject_missing_required_fields(client):
    # Missing amount
    payload = {
        "user_id": "U1001",
        "type": "credit",
        "timestamp": "2026-09-18T10:30:00",
    }
    response = client.post("/transactions", json=payload)
    assert response.status_code == 422


def test_reject_empty_user_id(client):
    payload = {
        "user_id": "",
        "amount": 100,
        "type": "credit",
        "timestamp": "2026-09-18T10:30:00",
    }
    response = client.post("/transactions", json=payload)
    assert response.status_code == 422
