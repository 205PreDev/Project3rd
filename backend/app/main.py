from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from app.core.config import settings
from app.core.database import create_db_and_tables
from app.api import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan events for FastAPI application"""
    # Startup: Create database tables
    await create_db_and_tables()
    yield
    # Shutdown: Cleanup (if needed)


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "message": "AI E-commerce Image Generator API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


# Include API routers
app.include_router(api_router, prefix=settings.API_V1_STR)

# Mount static files for uploaded images
uploads_dir = Path("./uploads")
uploads_dir.mkdir(exist_ok=True)
app.mount("/files", StaticFiles(directory=str(uploads_dir)), name="files")
