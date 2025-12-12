import logging
from fastapi import FastAPI, Request, Response
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.utils import get_openapi

from app.core.database import Base, engine
from app.core.middleware import UserActionLogMiddleware
from app.core.logging_config import setup_logging
from app.scheduler import start_scheduler
from app.domains.user.router import router as user_router
from app.domains.auth.router import router as auth_router
from app.domains.payment.routers import router as payment_router
from app.core.exception_handler import (
    app_exception_handler,
    unhandled_exception_handler,
    http_exception_handler,
    validation_exception_handler
)
from app.core.exceptions import AppException
from fastapi.exceptions import HTTPException, RequestValidationError

setup_logging()
logger = logging.getLogger("app")

app = FastAPI(
    title="FastAPI Example",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    swagger_ui_parameters={
        "defaultModelsExpandDepth": -1,
        "displayRequestDuration": True,
        "docExpansion": "none",
        "deepLinking": True
    }
)

@app.on_event("startup")
def startup_event():
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

    return Response(
        content=resp_body,
        status_code=response.status_code,
        headers=dict(response.headers),
        media_type=response.media_type
    )

app.mount("/static", StaticFiles(directory="uploads"), name="static")

app.add_middleware(UserActionLogMiddleware)
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# 라우터 등록 (tags 추가)
app.include_router(user_router, prefix="/api/v1/user", tags=["User"])
app.include_router(auth_router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(payment_router, prefix="/api/v1/payment", tags=["Payment"])

# OpenAPI 커스터마이징
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="히엘페이 API",
        version="1.0.0",
        description="히엘페이 프로젝트",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {"url": "https://example.com/logo.png"}
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
