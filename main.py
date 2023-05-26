from fastapi import FastAPI, Depends, HTTPException, status
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

@app.post("/auth/signup", tags=["auth"])
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db), api_key: str = Depends(api_key.verify_api_key)):
    if await crud.is_username_taken(db, username=user.username):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already registered")
    if await crud.is_email_taken(db, email=user.email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    
    await crud.create_user(db=db, user=user)
    if await crud.is_username_taken(db, username=user.username):
        raise HTTPException(status_code=status.HTTP_201_CREATED, detail="User created")
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="User not created")

@app.post("/auth/login", tags=["auth"])
async def login(user: schemas.UserLogin, db: Session = Depends(get_db), api_key: str = Depends(api_key.verify_api_key)):
    if await crud.login_verify(db=db, user=user):
        raise HTTPException(status_code=status.HTTP_200_OK, detail="Login successful")
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Login failed")

@app.post("/auth/key", tags=["auth"])
async def create_api_key(userData: schemas.UserAdminVerify, db: Session = Depends(get_db)):
    temp = await crud.create_api_key(db=db, userData=userData)
    if temp:
        raise HTTPException(status_code=status.HTTP_200_OK, detail=temp)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="YOU ARE NOT AN ADMIN")
