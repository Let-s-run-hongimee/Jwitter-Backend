from passlib.context import CryptContext

context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_hashing(plain_text, hashed_text):
    return context.verify(plain_text, hashed_text)

def hashing(non_hashed_text):
    return context.hash(non_hashed_text)