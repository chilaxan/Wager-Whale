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

def get_wagers(db: Session, user: schemas.User):
    return db.query(models.Wager).filter(models.Wager.owner == user.id).all()

def add_wager(db: Session, user: schemas.User, startX: float, startY: float, endX: float, endY: float, bet: float, duration: float, stream: str):
    if bet > user.balance or bet < 0 or duration < 0:
        return None
    db_wager = models.Wager(
        owner=user.id,
        startX = startX,
        startY = startY,
        endX = endX,
        endY = endY,
        bet = bet, 
        duration = duration,
        stream = stream
    )
    db.add(db_wager)
    user.balance -= bet
    db.add(user)
    db.commit()
    db.refresh(db_wager)
    db.refresh(user)
    return db_wager