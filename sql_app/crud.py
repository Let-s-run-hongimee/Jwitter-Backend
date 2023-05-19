from sqlalchemy.orm import Session
from . import models, schemas

# Create

def create_user(db: Session, user: schemas.UserCreate):
    

# Read

# Update

# Delete


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.userId == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()
    
def get_email_by_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.userId == user_id).first().email

def 

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = hash_password(user.password)  # Need to implement hash_password function
    db_user = models.User(email=user.email, username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Similarly, create CRUD functions for Tweet and Photo models
