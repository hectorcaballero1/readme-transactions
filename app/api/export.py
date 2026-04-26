from fastapi import APIRouter, HTTPException
from app.db.database import get_cursor

router = APIRouter(prefix="/api/export", tags=["export"])


@router.get("/transactions")
def export_transactions():
    try:
        with get_cursor() as cur:
            cur.execute("SELECT * FROM transactions ORDER BY created_at DESC")
            return cur.fetchall()
    except Exception:
        raise HTTPException(status_code=500, detail="internal server error")


@router.get("/reviews")
def export_reviews():
    try:
        with get_cursor() as cur:
            cur.execute("SELECT * FROM reviews ORDER BY created_at DESC")
            return cur.fetchall()
    except Exception:
        raise HTTPException(status_code=500, detail="internal server error")
