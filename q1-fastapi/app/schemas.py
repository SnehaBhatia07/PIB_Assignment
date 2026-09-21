from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field


class TransactionCreate(BaseModel):
    user_id: str = Field(..., min_length=1, description="Identifier of the user")
    amount: float = Field(..., gt=0, description="Transaction amount, must be positive")
    type: Literal["credit", "debit"] = Field(..., description="Transaction type: credit or debit")
    timestamp: datetime = Field(..., description="Transaction timestamp in ISO format")


class TransactionResponse(BaseModel):
    user_id: str
    amount: float
    type: Literal["credit", "debit"]
    timestamp: datetime


class TransactionSummary(BaseModel):
    total_credit: float
    total_debit: float
    balance: float
