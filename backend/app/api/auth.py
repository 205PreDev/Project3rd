from fastapi import APIRouter
from app.core.auth import auth_backend, fastapi_users
from app.schemas.user import UserRead, UserCreate, UserUpdate

router = APIRouter()

# Include authentication routes
router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/jwt",
)

# Include registration route
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
)

# Include user management routes (get current user, update, delete)
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
)

# Include password reset routes
router.include_router(
    fastapi_users.get_reset_password_router(),
)

# Include email verification routes
router.include_router(
    fastapi_users.get_verify_router(UserRead),
)
