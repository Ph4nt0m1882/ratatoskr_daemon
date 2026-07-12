from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scalar_fastapi import get_scalar_api_reference
from contextlib import asynccontextmanager

from app.core.config import settings
from app.api import routes
from app.db.database import create_db_and_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Runs on startup
    create_db_and_tables()
    yield
    # Runs on shutdown

app = FastAPI(
    title=settings.app_name, 
    description="Ratatoskr Local Brain API",
    lifespan=lifespan,
    docs_url=None,
)

# CORS configuration to allow requests from any origin (notably for flutter web)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for production allow only specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the API router with a prefix for versioning
app.include_router(routes.router)

@app.get("/")
async def root():
    return {"message": "Ratatoskr Daemon est en ligne. Utilisez /api/v1/health pour le statut."}

@app.get("/docs", include_in_schema=False)
async def scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
    )
