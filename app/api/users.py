from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.schemas.user_schema import UserCreate, UserLogin
from app.db.crud import create, read, update, delete
from app.utils.jwt import JWT

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

router = APIRouter()

@router.post("/signup")
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user_db = await create.create_user(db, user)
    if not user_db:
        raise HTTPException(status_code=409, detail="email or username is already registered")

    access_token = JWT.create_access_token(subject=user_db.id)
    refresh_token = JWT.create_refresh_token(subject=user_db.id)

    if await create.add_refresh_token(db, refresh_token, user_db.id):
        return {"access_token": access_token, "refresh_token": refresh_token}
    raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/login")
async def login(user: UserLogin, db: Session = Depends(get_db)):
     # Load AuthJWT

    user_db = await read.verify_user(db, user)
    if not user_db:
        raise HTTPException(status_code=401, detail="Invalid id or password")
    
    access_token = JWT.create_access_token(subject=user_db.id)
    refresh_token = JWT.create_refresh_token(subject=user_db.id)
    if await delete.delete_refresh_token_by_userId(db, user_db.id):
        await create.add_refresh_token(db, refresh_token, user_db.id)
        return {"access_token": access_token, "refresh_token": refresh_token}
    raise HTTPException(status_code=500, detail="Internal Server Error")
    

@router.get("/me")
async def get_current_user(db: Session = Depends(get_db), token: Annotated[str, Depends(oauth2_scheme)] = None):
    subject = JWT.verify_token_and_get_sub(token)
    print(subject)
    user_db = await read.get_user_by_user_id(db, subject)

    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "username" : user_db.username,
        "nickname" : user_db.nickname,
        "email" : user_db.email,
        "is_auth_user" : user_db.is_auth_user
    }

@router.put("/me/update")
async def update_nickname(nickname: str, db: Session = Depends(get_db), token: Annotated[str, Depends(oauth2_scheme)] = None):
    subject = JWT.verify_token_and_get_sub(token)

    if await update.update_user_nickname(db, nickname, subject):
        raise HTTPException(status_code=200, detail="Successfully updated")
    raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/refresh")
async def refresh(db: Session = Depends(get_db), token: Annotated[str, Depends(oauth2_scheme)] = None):
    subject = JWT.verify_token_and_get_sub(token)
    if await read.verify_refresh_token(db, token, subject):
        access_token = JWT.create_access_token(subject=subject)
        return {"access_token": access_token}
    raise HTTPException(status_code=401, detail="Invalid refresh token")

@router.post("/logout")
async def logout(db: Session = Depends(get_db), token: Annotated[str, Depends(oauth2_scheme)] = None):
    subject = JWT.verify_token_and_get_sub(token)

    if await delete.delete_refresh_token_by_userId(db, subject):
        raise HTTPException(status_code=200, detail="Successfully logged out")
    raise HTTPException(status_code=500, detail="Internal Server Error")
