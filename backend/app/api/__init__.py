from fastapi import APIRouter
from app.api import auth
from app.api.endpoints import projects, images, credits

api_router = APIRouter()

# Include authentication routes
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

# Include endpoint routes
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(images.router, prefix="/images", tags=["images"])
api_router.include_router(credits.router, prefix="/credits", tags=["credits"])
