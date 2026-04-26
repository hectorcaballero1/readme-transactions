from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class ReviewCreate(BaseModel):
    target_user_id: int
    transaction_id: Optional[int] = None
    rating: float = Field(..., ge=1, le=5)
    comment: Optional[str] = None


class Review(BaseModel):
    id: int
    user_id: int
    target_user_id: int
    transaction_id: Optional[int]
    rating: float
    comment: Optional[str]
    created_at: datetime


class ReviewStats(BaseModel):
    average_rating: Optional[float]
    total_reviews: int
