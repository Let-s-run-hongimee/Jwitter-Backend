class Settings():
    authjwt_secret_key: str = "hongimee_secret_key"
    authjwt_algorithm: str = "HS256"

def get_settings():
    return Settings()
