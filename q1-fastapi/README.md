# Q1: Transaction Processing API

A RESTful backend service built using FastAPI to process credit and debit transactions, query a user's transaction history, and generate balance summaries.

## How to Run
1. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the application:
   ```bash
   uvicorn app.main:app --reload
   ```
4. Access Swagger UI at `http://127.0.0.1:8000/docs`.

## How to Test on Your Screen
1. Open `http://127.0.0.1:8000/docs` in your browser.
2. Click `POST /transactions` -> click **Try it out**.
3. Send sample JSON:
   ```json
   {
     "user_id": "U1001",
     "amount": 1500,
     "type": "credit",
     "timestamp": "2026-09-18T10:30:00"
   }
   ```
4. Click **Execute** and observe HTTP `201 Created` on screen.
5. Click `GET /transactions/U1001` to view the list of transactions.
6. Click `GET /transactions/U1001/summary` to view the balance calculation.
7. Test validation by sending a negative amount (`-100`) and verifying HTTP `422` error on screen.

## Running Tests
```bash
pytest -v
```
All 13 test cases pass.
