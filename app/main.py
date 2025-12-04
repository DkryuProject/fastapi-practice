from fastapi import FastAPI
from app.core.database import Base, engine
import app.domains.user.models as user_models
from app.domains.user.router import router as user_router
from app.domains.auth.router import router as auth_router

# create tables (for dev; production은 Alembic 추천)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI + MySQL + JWT Template")

app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
