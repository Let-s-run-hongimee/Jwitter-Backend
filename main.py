from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasicCredentials
from sqlalchemy.orm import Session
from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine
from sql_app.utils import api_key

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db), api_key: str = Depends(api_key.verify_api_key)):
    if await crud.is_username_taken(db, username=user.username):
        raise HTTPException(status_code=400, detail="Username already registered")
    if await crud.is_email_taken(db, email=user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    await crud.create_user(db=db, user=user)
    if await crud.is_username_taken(db, username=user.username):
        raise HTTPException(status_code=200, detail="User created")
    raise HTTPException(status_code=400, detail="User not created")



@app.post("/api-keys/", response_model=schemas.APIKey)
async def create_api_key(api_key: schemas.APIKeyCreate, db: Session = Depends(get_db), credentials: HTTPBasicCredentials = Depends(api_key.verify_credentials)):
    return await crud.create_api_key(db=db, key=api_key.key)
