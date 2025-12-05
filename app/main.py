import logging
from fastapi import FastAPI, Request, Response
from app.core.database import Base, engine
from app.domains.user.router import router as user_router
from app.domains.auth.router import router as auth_router
from app.core.middleware import UserActionMiddleware
from app.core.logging_config import setup_logging

setup_logging()
logger = logging.getLogger("app")

# create tables (for dev; production은 Alembic 추천)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI + MySQL + JWT Template")

@app.middleware("http")
async def full_request_response_logger(request: Request, call_next):
    body = await request.body()
    logger.info(f"[REQUEST BODY] {body}")

    response = await call_next(request)

    response_body = b""
    async for chunk in response.body_iterator:
        response_body += chunk
    logger.info(f"[RESPONSE BODY] {response_body}")

    return Response(
        content=response_body,
        status_code=response.status_code,
        headers=dict(response.headers),
        media_type=response.media_type,
    )

app.add_middleware(UserActionMiddleware)

app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
