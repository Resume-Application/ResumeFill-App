from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import settings
from app.core.db import init_db
from app.routers import auth_routes, company_routes, job_position_routes, users_routes, application_routes

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


app.include_router(auth_routes.router, tags=["Authentication"])
app.include_router(users_routes.router, tags=["Users"])
app.include_router(application_routes.router, tags=["Application"])
app.include_router(company_routes.router, tags=["Company"])
app.include_router(job_position_routes.router, tags=["Job Positions"])
@app.get("/")
async def root():
    return {"message": "Welcome to FastAutofill Backend"}
