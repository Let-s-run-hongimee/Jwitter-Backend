import secrets
from fastapi import Request, HTTPException, status, Depends
from sqlalchemy.orm import Session
from sql_app import crud
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sql_app.database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def verify_api_key(request: Request, db: Session = Depends(get_db)):
    api_key = request.headers.get("X-API-KEY")
    username = request.headers.get("X-USER-NAME")
    if api_key is None or username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key or User id header is missing",
        )
    if not await crud.is_api_key_valid(db, api_key, username):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
        )
    return api_key

