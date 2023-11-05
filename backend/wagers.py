import streams
import threading
import time
import random
import crud

from database import SessionLocal
from yolofish.YOLOFISHGAMBLE import detect

def orderSlice(v1, v2):
    return slice(min(int(v1), int(v2)), max(int(v1), int(v2)))

def detectFish(frame, wager):
    crop = frame[orderSlice(wager.startY, wager.endY), orderSlice(wager.startX, wager.endX)]
    return detect(crop)

def calculateWinnings(wager):
    return wager.bet * 2

def calculateLoss(wager):
    return wager.bet

def wagerTarget(wager):
    db = SessionLocal()
    end = time.time() + wager.duration * 1000 # seconds to ms
    user = crud.get_user(db, wager.owner)
    while time.time() < end:
        frame = streams.rawStreamFrames[wager.stream]
        if detectFish(frame, wager):
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