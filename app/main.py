import logging
import json

from fastapi import FastAPI, Request, Response
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.utils import get_openapi
from pathlib import Path

from app.core.database import Base, engine
from app.core.middleware import UserActionLogMiddleware
from app.core.logging_config import setup_logging
from app.scheduler import start_scheduler
from app.domains.user.router import router as user_router
from app.domains.auth.router import router as auth_router
from app.domains.payment.routers import router as payment_router
from app.domains.view.router import router as view_router
from app.core.exception_handler import (
    app_exception_handler,
    unhandled_exception_handler,
    http_exception_handler,
    validation_exception_handler
)
from app.core.exceptions import AppException
from fastapi.exceptions import HTTPException, RequestValidationError
from app.core.templates import templates

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


SENSITIVE_KEYS = {"password", "access_token", "refresh_token", "card_number", "expire_month"}
MAX_BODY_LENGTH = 1000


def safe_decode(body: bytes) -> str:
    return body.decode("utf-8", errors="ignore")


def mask_sensitive(data: dict) -> dict:
    return {
        k: ("***" if k in SENSITIVE_KEYS else v)
        for k, v in data.items()
    }


@app.middleware("http")
async def full_logger(request: Request, call_next):
    content_type = request.headers.get("content-type", "")

    # -------- Request --------
    body_bytes = await request.body()
    request._body = body_bytes

    if body_bytes and "application/json" in content_type:
        try:
            body_json = json.loads(body_bytes.decode("utf-8"))
            body_json = mask_sensitive(body_json)
            body_log = json.dumps(body_json, ensure_ascii=False)
        except Exception:
            body_log = body_bytes.decode("utf-8", errors="ignore")

        logger.info(
            "[REQUEST] %s %s body=%s",
            request.method,
            request.url.path,
            body_log
        )

    elif body_bytes and "multipart/form-data" in content_type:
        logger.info(
            "[REQUEST] %s %s (multipart/form-data, body=%d bytes)",
            request.method,
            request.url.path,
            len(body_bytes)
        )

    else:
        logger.info(
            "[REQUEST] %s %s",
            request.method,
            request.url.path
        )

    # -------- Response --------
    response = await call_next(request)

    resp_body = b""
    async for chunk in response.body_iterator:
        resp_body += chunk

    if response.status_code >= 400:
        body_text = resp_body.decode("utf-8", errors="ignore")
        logger.error(
            "[RESPONSE] %s status=%s body=%s",
            request.url.path,
            response.status_code,
            body_text
        )
    else:
        logger.info(
            "[RESPONSE] %s status=%s",
            request.url.path,
            response.status_code
        )

    return Response(
        content=resp_body,
        status_code=response.status_code,
        headers=dict(response.headers),
        media_type=response.media_type
    )


BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"

UPLOAD_DIR.mkdir(exist_ok=True)

app.mount("/static", StaticFiles(directory=UPLOAD_DIR), name="static")

app.add_middleware(UserActionLogMiddleware)
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# 라우터 등록 (tags 추가)
app.include_router(user_router, prefix="/api/v1/user", tags=["User"])
app.include_router(auth_router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(payment_router, prefix="/api/v1/payment", tags=["Payment"])
app.include_router(view_router, prefix="/api/v1/view", tags=["View"])

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
