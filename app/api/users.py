from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.schemas.user_schema import UserCreate, UserLogin
from app.db.crud import create, read, update, delete
from fastapi_jwt_auth import AuthJWT

router = APIRouter()

@router.post("/signup")
async def create_user(request: Request, user: UserCreate, db: Session = Depends(get_db)):
    Authorize: AuthJWT = request.state.auth # Load AuthJWT
    
    user_db = await create.create_user(db, user)
    if not user_db:
        raise HTTPException(status_code=409, detail="email or username is already registered")
    
    access_token = Authorize.create_access_token(subject=user_db.user_id)
    refresh_token = Authorize.create_refresh_token(subject=user_db.user_id)
    await create.add_refresh_token(db, refresh_token, user_db.user_id)
    return {"access_token": access_token, "refresh_token": refresh_token}


@router.post("/login")
async def login(request: Request, user: UserLogin, db: Session = Depends(get_db)):
    Authorize: AuthJWT = request.state.auth # Load AuthJWT

    user_db = await read.login_verify(db, user)
    if not user_db:
        raise HTTPException(status_code=401, detail="Invalid id or password")
    
    access_token = Authorize.create_access_token(subject=user_db.user_id)
    refresh_token = Authorize.create_refresh_token(subject=user_db.user_id)
    await delete.delete_refresh_token_by_userId(db, user_db.user_id)
    await create.add_refresh_token(db, refresh_token, user_db.user_id)
    return {"access_token": access_token, "refresh_token": refresh_token}
