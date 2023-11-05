from sqlalchemy.orm import Session
import models, schemas
import utils

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate, balance: int):
    db_user = models.User(username=user.username, hashed_password=utils.get_hashed_password(user.password), balance=balance)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user