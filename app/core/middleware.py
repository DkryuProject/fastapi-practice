from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.domains.log.crud import create_log
from app.core.jwt import decode_token
from jose import JWTError


class UserActionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        db: Session = SessionLocal()

        # 기본값
        user_id = None

        # Access Token 에서 user_id 추출
        auth = request.headers.get("Authorization")
        if auth and auth.startswith("Bearer "):
            token = auth.split(" ")[1]
            try:
                payload = decode_token(token)
                if payload.get("type") == "access":
                    user_id = int(payload.get("sub"))
            except JWTError:
                pass

        # 클라이언트 정보
        client_ip = request.client.host if request.client else None
        user_agent = request.headers.get("User-Agent")

        # 로깅
        create_log(
            db=db,
            user_id=user_id,
            action=request.url.path,
            endpoint=str(request.url.path),
            method=request.method,
            client_ip=client_ip,
            user_agent=user_agent,
        )

        response = await call_next(request)
        return response
