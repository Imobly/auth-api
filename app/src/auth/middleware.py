from typing import List, Optional

from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.src.auth.security import decode_access_token


class AuthMiddleware(BaseHTTPMiddleware):
    PUBLIC_ROUTES = [
        "/",
        "/health",
        "/api/v1/docs",
        "/api/v1/openapi.json",
        "/api/v1/redoc",
        "/api/v1/auth/register",
        "/api/v1/auth/login",
    ]

    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        if self._is_public_route(path):
            response = await call_next(request)
            return response

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Token de autenticação é necessário"},
            )

        try:
            scheme, token = auth_header.split()
            if scheme.lower() != "bearer":
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": "Esquema de autenticação inválido. Use 'Bearer'"},
                )
        except ValueError:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Formato do header Authorization inválido"},
            )

        payload = decode_access_token(token)
        if payload is None:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Token inválido ou expirado"},
            )

        request.state.user_id = payload.get("sub")
        request.state.username = payload.get("username")

        response = await call_next(request)
        return response

    def _is_public_route(self, path: str) -> bool:
        if path in self.PUBLIC_ROUTES:
            return True

        public_prefixes = ["/uploads/", "/static/"]
        for prefix in public_prefixes:
            if path.startswith(prefix):
                return True

        return False
