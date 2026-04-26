from pydantic import BaseModel
from datetime import date
from typing import Optional

class TransactionBase(BaseModel):
    property_name: str
    category: str
    price: float
    quantity: int
    date: date

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int

    class Config:
        from_attributes = True # Allows Pydantic to work with SQLAlchemy models


class UserCreate(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str