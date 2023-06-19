from pydantic import BaseModel

class Settings(BaseModel):
    authjwt_secret_key: str = "hongimee_secret_key"

def get_settings():
    return Settings()
