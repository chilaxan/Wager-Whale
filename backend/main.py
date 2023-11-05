from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Request, Response, Cookie
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

import crud, models, schemas, utils, wagers
from streams import streams, makeStream, streamFrames
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def authentication(auth: Annotated[str | None, Cookie()] = None, db: Session = Depends(get_db)):
    if auth:
        data = utils.decode(auth)
        if data:
            return crud.get_user(db, data.get('id'))
    raise HTTPException(status_code=400, detail="Failed To authenticate")

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/login", response_model=schemas.User)
def login(logging_in_user: schemas.UserLogin, response: Response, db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, username=logging_in_user.username)
    if user and utils.check_password(logging_in_user.password, user.hashed_password):
        response.set_cookie("auth", utils.sign({'id': user.id}))
        return user
    raise HTTPException(status_code=400, detail="Failed To login")

@app.post('/logout')
def logout(response: Response) -> None:
    response.delete_cookie("auth")

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, response: Response, db: Session = Depends(get_db)):
    user.username = user.username.strip()
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    if not utils.check_username(user.username):
        raise HTTPException(status_code=400, detail="Invalid Username")
    newUser = crud.create_user(db=db, user=user, balance=100.0)
    response.set_cookie("auth", utils.sign({"id": newUser.id}))
    return newUser

@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return sorted(users, key=lambda u: u.balance, reverse=True)

@app.get("/self", response_model=schemas.User)
def get_self(user = Depends(authentication)):
    return user

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.get("/streams", response_model=list[schemas.Stream])
def get_streams(user = Depends(authentication)):
    return streams

@app.get("/streams/{stream_id}")
def get_stream(stream_id: str, user = Depends(authentication)):
    if stream_id not in streamFrames:
        raise HTTPException(status_code=404, detail="Stream not found")
    return StreamingResponse(makeStream(stream_id), media_type='multipart/x-mixed-replace; boundary=frame')

@app.get("/wagers", response_model=list[schemas.Wager])
def get_wagers(db: Session = Depends(get_db), user = Depends(authentication)):
    return crud.get_wagers(db, user=user)

@app.post("/wagers/", response_model=schemas.Wager)
def make_wager(wager: schemas.WagerCreate, db: Session = Depends(get_db), user = Depends(authentication)):
    if wager.stream not in streamFrames:
        raise HTTPException(status_code=404, detail="Stream not found")
    wager.bet = round(wager.bet, 2)
    newWager = crud.add_wager(db, user,
                                startX = wager.startX,
                                startY = wager.startY,
                                endX = wager.endX,
                                endY = wager.endY,
                                bet = wager.bet,
                                duration= wager.duration,
                                stream = wager.stream)
    if newWager is None:
        raise HTTPException(status_code=400, detail="Invalid Wager")
    wagers.launchWager(newWager)
    return newWager

@app.get("/notifications", response_model=list[schemas.WagerNotification])
def get_notifications(user = Depends(authentication)):
    return wagers.notifications.pop(user.id, [])