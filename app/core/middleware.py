from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from app.domains.user.models import UserActionLog
from app.core.database import SessionLocal
import traceback
from datetime import datetime


class UserActionLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # DB 세션 생성
        db = SessionLocal()

        # 기본 정보
        client_ip = request.client.host if request.client else None
        user_agent = request.headers.get("User-Agent", "")

        # 요청 처리 전 user_id 확보
        # - JWT 인증 dependency 에서: request.state.user_id = user.id 를 입력해줘야 함
        user_id = getattr(request.state, "user_id", None)

        try:
            response: Response = await call_next(request)

            # 요청 후 저장
            log = UserActionLog(
                user_id=user_id,
                action=request.url.path,
                endpoint=str(request.url.path),
                method=request.method,
                client_ip=client_ip,
                user_agent=user_agent,
                created_at=datetime.utcnow()
            )

            db.add(log)
            db.commit()

        except Exception as e:
            db.rollback()
            print("UserActionLog Error:", e)
            traceback.print_exc()
            raise e

        finally:
            db.close()

        return response
