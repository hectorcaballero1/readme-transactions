import psycopg2
from psycopg2.extras import RealDictCursor
from app.core.config import settings

_conn = None


def get_connection():
    global _conn
    if _conn is None or _conn.closed:
        _conn = psycopg2.connect(
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            dbname=settings.DB_NAME,
            cursor_factory=RealDictCursor,
        )
    return _conn


def get_cursor():
    return get_connection().cursor(cursor_factory=RealDictCursor)


def create_tables():
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id SERIAL PRIMARY KEY,
                book_id INT NOT NULL,
                buyer_id INT NOT NULL,
                seller_id INT NOT NULL,
                created_at TIMESTAMP DEFAULT NOW()
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS reviews (
                id SERIAL PRIMARY KEY,
                user_id INT NOT NULL,
                target_user_id INT NOT NULL,
                transaction_id INT REFERENCES transactions(id),
                rating FLOAT CHECK (rating >= 1 AND rating <= 5),
                comment TEXT,
                created_at TIMESTAMP DEFAULT NOW()
            )
        """)
    conn.commit()
