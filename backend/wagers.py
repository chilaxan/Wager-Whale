import streams
import threading
import time
import random
import crud

from database import SessionLocal

def detectFish(frame, wager):
    return random.choice([True] + [False] * 9)

def calculateWinnings(wager):
    return wager.bet + 5

def calculateLoss(wager):
    return wager.bet - 5

def wagerTarget(wager):
    db = SessionLocal()
    end = time.time() + wager.duration * 1000 # seconds to ms
    user = crud.get_user(db, wager.owner)
    while time.time() < end:
        frame = streams.streamFrames[wager.stream].cell_contents
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