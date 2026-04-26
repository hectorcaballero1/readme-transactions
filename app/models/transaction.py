from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Generic, TypeVar

T = TypeVar("T")


class PagedResponse(BaseModel, Generic[T]):
    data: list
    total: int
    page: int
    size: int
    total_pages: int


class TransactionCreate(BaseModel):
    book_id: int
    buyer_id: int
    seller_id: int


class Transaction(BaseModel):
    id: int
    book_id: int
    buyer_id: int
    seller_id: int
    created_at: datetime
