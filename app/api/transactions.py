from fastapi import APIRouter, HTTPException, Query, Request
from app.db.database import get_connection, get_cursor
from app.models.transaction import Transaction, TransactionCreate, PagedResponse

router = APIRouter(prefix="/api/transactions", tags=["transactions"])


@router.get("", response_model=PagedResponse)
def list_transactions(page: int = Query(1, ge=1), size: int = Query(20, ge=1, le=100)):
    offset = (page - 1) * size
    try:
        with get_cursor() as cur:
            cur.execute("SELECT COUNT(*) AS total FROM transactions")
            total = cur.fetchone()["total"]
            cur.execute(
                "SELECT * FROM transactions ORDER BY created_at DESC LIMIT %s OFFSET %s",
                (size, offset),
            )
            data = cur.fetchall()
    except Exception:
        raise HTTPException(status_code=500, detail="internal server error")
    return {
        "data": data,
        "total": total,
        "page": page,
        "size": size,
        "total_pages": max(1, -(-total // size)),
    }


@router.get("/book/{book_id}", response_model=list[Transaction])
def get_by_book(book_id: int):
    try:
        with get_cursor() as cur:
            cur.execute(
                "SELECT * FROM transactions WHERE book_id = %s ORDER BY created_at DESC",
                (book_id,),
            )
            return cur.fetchall()
    except Exception:
        raise HTTPException(status_code=500, detail="internal server error")


@router.get("/user/{user_id}", response_model=list[Transaction])
def get_by_user(user_id: int):
    try:
        with get_cursor() as cur:
            cur.execute(
                "SELECT * FROM transactions WHERE buyer_id = %s OR seller_id = %s ORDER BY created_at DESC",
                (user_id, user_id),
            )
            return cur.fetchall()
    except Exception:
        raise HTTPException(status_code=500, detail="internal server error")


@router.get("/{transaction_id}", response_model=Transaction)
def get_transaction(transaction_id: int):
    try:
        with get_cursor() as cur:
            cur.execute("SELECT * FROM transactions WHERE id = %s", (transaction_id,))
            row = cur.fetchone()
    except Exception:
        raise HTTPException(status_code=500, detail="internal server error")
    if not row:
        raise HTTPException(status_code=404, detail="not found")
    return row


@router.post("", response_model=Transaction, status_code=201)
def create_transaction(body: TransactionCreate):
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO transactions (book_id, buyer_id, seller_id)
                VALUES (%s, %s, %s)
                RETURNING *
                """,
                (body.book_id, body.buyer_id, body.seller_id),
            )
            row = dict(cur.fetchone())
        conn.commit()
        return row
    except Exception:
        raise HTTPException(status_code=500, detail="internal server error")
