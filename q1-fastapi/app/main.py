from fastapi import FastAPI, status
from app.schemas import TransactionCreate, TransactionResponse, TransactionSummary
from app import service

app = FastAPI(
    title="Transaction Processing API",
    description="API for processing and summarizing credit and debit transactions.",
)


@app.post(
    "/transactions",
    status_code=status.HTTP_201_CREATED,
    response_model=TransactionResponse,
)
def create_transaction(transaction: TransactionCreate):
    return service.create_transaction(transaction)


@app.get(
    "/transactions/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=list[TransactionResponse],
)
def get_transactions(user_id: str):
    return service.get_transactions(user_id)


@app.get(
    "/transactions/{user_id}/summary",
    status_code=status.HTTP_200_OK,
    response_model=TransactionSummary,
)
def get_user_summary(user_id: str):
    return service.get_user_summary(user_id)
