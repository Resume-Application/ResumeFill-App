from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import settings
from app.core.db import init_db
from app.routers import auth

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

#from app.middleware.auth import AuthMiddleware

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)

#app.add_middleware(AuthMiddleware)


app.include_router(auth.router, tags=["Authentication"])

@app.get("/")
async def root():
    return {"message": "Welcome to FastAutofill Backend"}
