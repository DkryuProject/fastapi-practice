import logging
from fastapi import FastAPI, Request, Response
from app.core.database import Base, engine
from app.domains.user.router import router as user_router
from app.domains.auth.router import router as auth_router
from app.core.middleware import UserActionLogMiddleware
from app.core.logging_config import setup_logging
from app.scheduler import start_scheduler
from app.domains.payment.routers import payment_routers
from starlette.responses import Response
from app.core.exception_handler import (
    app_exception_handler,
    unhandled_exception_handler,
    http_exception_handler,
    validation_exception_handler
)
from app.core.exceptions import AppException
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.staticfiles import StaticFiles

setup_logging()
logger = logging.getLogger("app")

app = FastAPI(title="FastAPI")


@app.on_event("startup")
def startup_event():
    # DEV ONLY — production = alembic
    Base.metadata.create_all(bind=engine)
    start_scheduler()


@app.middleware("http")
async def full_logger(request: Request, call_next):
    req_body = await request.body()
    logger.info(f"[REQUEST BODY] {req_body}")

    response = await call_next(request)

    resp_body = b""
    async for chunk in response.body_iterator:
        resp_body += chunk

    logger.info(f"[RESPONSE BODY] {resp_body}")

    # 새로운 Response 생성 → content-length 자동 계산
    return Response(
        content=resp_body,
        status_code=response.status_code,
        headers=dict(response.headers),
        media_type=response.media_type
    )


# 로컬 파일 접근 가능하게
app.mount("/static", StaticFiles(directory="uploads"), name="static")


app.add_middleware(UserActionLogMiddleware)
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

app.include_router(user_router, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1")

for router in payment_routers:
    app.include_router(router, prefix="/api/v1")
