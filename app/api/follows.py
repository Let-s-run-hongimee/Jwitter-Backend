from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.crud import create, read, update, delete
from app.utils.jwt import JWT

router = APIRouter()

@router.post("/following/{following_id}")
async def follow_user(request: Request, following_id: int, db: Session = Depends(get_db)):
    
    decode_access_token(request.cookies['access_token_cookie'])
    current_user = int(decode_access_token(request.cookies['access_token_cookie'])['sub'])

    if current_user == following_id:
        raise HTTPException(status_code=400, detail="You cannot follow yourself")

    user_db = await read.get_user_by_user_id(db, following_id)
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")

    if await read.is_following(db, following_id, current_user):
        raise HTTPException(status_code=400, detail="You are already following this user")

    await create.follow_user(db, current_user, following_id)
    return {"message": "Successfully followed"}

@router.delete("/unfollowing/{followed_id}")
async def unfollow_user(request: Request, followed_id: int, db: Session = Depends(get_db)):
    
    decode_access_token(request.cookies['access_token_cookie'])
    current_user = int(decode_access_token(request.cookies['access_token_cookie'])['sub'])

    if current_user == followed_id:
        raise HTTPException(status_code=400, detail="You cannot unfollow yourself")

    user_db = await read.get_user_by_user_id(db, followed_id)
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")

    if not await read.is_following(db, followed_id, current_user):
        raise HTTPException(status_code=400, detail="You are not following this user")

    await delete.unfollow_user(db, current_user, followed_id)
    return {"message": "Successfully unfollowed"}