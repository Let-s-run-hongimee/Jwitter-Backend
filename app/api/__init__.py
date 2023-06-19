from fastapi import APIRouter
from app.api import users
from app.core.config import Settings
from fastapi_jwt_auth import AuthJWT

@AuthJWT.load_config
def get_config():
    return Settings()

router = APIRouter()

router.include_router(users.router, tags=["auth"], prefix="/auth")
