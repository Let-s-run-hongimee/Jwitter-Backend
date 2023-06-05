from fastapi import FastAPI, Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

@AuthJWT.load_config
def get_config():
    return schemas.Settings()

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/user/signup", tags=["user"])
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if await crud.is_username_taken(db, username=user.username):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already registered")
    if await crud.is_email_taken(db, email=user.email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    
    await crud.create_user(db=db, user=user)
    # 예외 처리 : create_user() 함수가 정상적으로 실행되지 않았을 때
    if await crud.is_username_taken(db, username=user.username):
        raise HTTPException(status_code=status.HTTP_201_CREATED, detail="User created")
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="User not created")

@app.post("/user/login", tags=["user"])
async def login(user: schemas.UserLogin, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    if not await crud.login_verify(db=db, user=user):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Login failed")
    
    access_token = Authorize.create_access_token(subject=user.id)
    return {"access_token": access_token}

# Create Tweet
@app.post("/tweet/create", tags=["protected"])
async def create_tweet(tweet: schemas.TweetCreate, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    return await crud.create_tweet(db=db, tweet=tweet, login_id=current_user)

# Get All Tweets (self)
@app.get("/tweet/all", tags=["protected"])
async def get_all_tweets(db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    return await crud.get_all_tweets(db=db, login_id=current_user)

# Update Tweet

# Delete Tweet

@app.get('/protected', tags=["protected"])
def protected(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    return {"logged_in_as": current_user}