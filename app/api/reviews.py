from fastapi import APIRouter, HTTPException, Query, Request
from app.db.database import get_connection, get_cursor
from app.models.review import Review, ReviewCreate, ReviewStats
from app.models.transaction import PagedResponse

router = APIRouter(prefix="/api/reviews", tags=["reviews"])


@router.post("", response_model=Review, status_code=201)
def create_review(body: ReviewCreate, request: Request):
    user_id = request.state.user_id
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO reviews (user_id, target_user_id, transaction_id, rating, comment)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING *
                """,
                (user_id, body.target_user_id, body.transaction_id, body.rating, body.comment),
            )
            row = dict(cur.fetchone())
        conn.commit()
        return row
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="internal server error")


@router.get("/user/{user_id}", response_model=PagedResponse)
def get_reviews_by_user(
    user_id: int,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
):
    offset = (page - 1) * size
    try:
        with get_cursor() as cur:
            cur.execute(
                "SELECT COUNT(*) AS total FROM reviews WHERE target_user_id = %s",
                (user_id,),
            )
            total = cur.fetchone()["total"]
            cur.execute(
                "SELECT * FROM reviews WHERE target_user_id = %s ORDER BY created_at DESC LIMIT %s OFFSET %s",
                (user_id, size, offset),
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


@router.get("/stats/{user_id}", response_model=ReviewStats)
def get_review_stats(user_id: int):
    try:
        with get_cursor() as cur:
            cur.execute(
                "SELECT AVG(rating) AS average_rating, COUNT(*) AS total_reviews "
                "FROM reviews WHERE target_user_id = %s",
                (user_id,),
            )
            row = cur.fetchone()
        return {
            "average_rating": float(row["average_rating"]) if row["average_rating"] is not None else None,
            "total_reviews": row["total_reviews"],
        }
    except Exception:
        raise HTTPException(status_code=500, detail="internal server error")
