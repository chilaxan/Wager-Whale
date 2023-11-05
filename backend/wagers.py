import cv2
import streams
import threading
import time
import crud
import random

from database import SessionLocal
from yolofish.YOLOFISHGAMBLE import detect

def orderSlice(v1, v2):
    return slice(min(int(v1), int(v2)), max(int(v1), int(v2)))

def detectFish(frame, wager):
    crop = frame[orderSlice(wager.startY, wager.endY), orderSlice(wager.startX, wager.endX)]
    return detect(crop)


def CalcPayout(X,Y,XResolution,YResolution,Bet,Time):
    ResProb = (X*Y)/(XResolution*YResolution)
    ResProbo = 1-(ResProb**2)
    TimeProb = Time/300
    TimeProbo = (TimeProb - 1)**2
    Prob = ResProbo+TimeProbo
    Winnings = Prob*Bet
    return round(Winnings, 2)

XResolution = 1920
YResolution = 1080

def calculateWinnings(wager):
    return CalcPayout(wager.startX, wager.startY, XResolution, YResolution, wager.bet, wager.duration)

def calculateLoss(wager):
    return CalcPayout(wager.startX, wager.startY, XResolution, YResolution, wager.bet, wager.duration)

def wagerTarget(wager):
    db = SessionLocal()
    end = time.time() + (wager.duration * 1000) # seconds to ms
    user = crud.get_user(db, wager.owner)
    while time.time() < end:
        frame = streams.rawStreamFrames[wager.stream]
        if detectFish(frame, wager): # add some randomness, our model is not reliable yet
            winnings = calculateWinnings(wager)
            user.balance += wager.bet + winnings
            db.add(user)
            db.commit()
            db.refresh(user)
            db.delete(wager)
            db.commit()
            notifications.setdefault(user.id, []).append({
                'message': f'Your Wager Hit! You won {winnings}',
                'delta': wager.bet + winnings
            })
            db.close()
            return
        time.sleep(0.5)
    loss = calculateLoss(wager)
    user.balance += wager.bet - loss
    db.add(user)
    db.commit()
    db.refresh(user)
    db.delete(wager)
    db.commit()
    notifications.setdefault(user.id, []).append({
        'message': f'Your Wager Did Not Hit! You lost {loss}',
        'delta': wager.bet - loss
    })
    db.close()

wagerThreads = []

def launchWager(wager):
    t = threading.Thread(target=wagerTarget, args=(wager, ))
    t.setDaemon(True)
    wagerThreads.append(t)
    t.start()

notifications = {}