from pydantic import BaseModel

class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str

class UserLogin(UserBase):
    password: str

class User(UserBase):
    id: int
    balance: int

    class Config:
        orm_mode = True

class Stream(BaseModel):
    id: str
    label: str
    weight: float