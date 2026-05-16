from fastapi import Request
from fastapi.responses import JSONResponse
from jose import jwt, JWTError
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.config import settings

UNPROTECTED_PATHS = {"/docs", "/openapi.json", "/redoc", "/health"}


class JWTMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.method == "OPTIONS" or request.url.path in UNPROTECTED_PATHS:
            return await call_next(request)

        if request.url.path.startswith("/api/export"):
            admin_key = request.headers.get("X-API-Key", "")
            if admin_key != settings.ADMIN_KEY:
                return JSONResponse(status_code=401, content={"error": "unauthorized"})
            return await call_next(request)

        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return JSONResponse(status_code=401, content={"error": "unauthorized"})

        token = auth_header.removeprefix("Bearer ").strip()
        try:
            payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
            request.state.user_id = payload.get("user_id")
        except JWTError:
            return JSONResponse(status_code=401, content={"error": "unauthorized"})

        return await call_next(request)
