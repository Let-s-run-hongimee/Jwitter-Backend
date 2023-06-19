from fastapi import FastAPI, Request
from app.api import router as api_router
from fastapi_jwt_auth import AuthJWT
from app.db.session import SessionLocal, engine
from app.db.models import user_model, tweet_model

user_model.Base.metadata.create_all(bind=engine)
tweet_model.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(api_router)

@app.middleware("http")
async def load_jwt_to_request(request: Request, call_next):
    request.state.auth = AuthJWT()  # `AuthJWT` 인스턴스를 request.state에 저장
    response = await call_next(request)
    return response