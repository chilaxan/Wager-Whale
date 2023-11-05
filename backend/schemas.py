from pydantic import BaseModel

class WagerBase(BaseModel):
    startX: float
    startY: float
    endX: float
    endY: float
    bet: float
    duration: float
    stream: str

class Wager(WagerBase):
    id: int
    owner: int

class WagerCreate(WagerBase):
    pass

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class UserLogin(UserBase):
    password: str

class User(UserBase):
    id: int
    balance: float

    class Config:
        from_attributes = True

class Stream(BaseModel):
    id: str
    label: str
    weight: float

class WagerNotification(BaseModel):
    delta: float
    message: str