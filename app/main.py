from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException, RequestValidationError
from app.core.config import settings
from app.db.database import create_tables
from app.middleware.auth import JWTMiddleware
from app.api import transactions, reviews, export

app = FastAPI(
    title="readme-transactions",
    description="Microservicio de transacciones y reseñas de libros",
    version="1.0.0",
)

origins = [o.strip() for o in settings.ALLOWED_ORIGINS.split(",") if o.strip()] or ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "X-Admin-Key"],
)
app.add_middleware(JWTMiddleware)

app.include_router(transactions.router)
app.include_router(reviews.router)
app.include_router(export.router)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    first = exc.errors()[0]
    msg = first.get("msg", "invalid request")
    return JSONResponse(status_code=400, content={"error": msg})


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"error": "internal server error"})


@app.on_event("startup")
def startup():
    create_tables()
