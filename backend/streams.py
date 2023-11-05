import threading
import requests
import cv2
import time
from types import CellType

#streamRelay = 'https://relay.ozolio.com/ses.api?cmd=open&oid={}&output=1&format=M3U8&profile=AUTO'

streams = [
    {
        'label': 'JellyFish',
        'id': 'JellyFish',
        'weight': 0.8,
        'url': 'https://streams.chilaxan.cc/JellyFish.mp4.m3u8' # 'https://usw01-smr04-relay.ozolio.com/hll-live/_definst_/relay01.bktacf0.fd0.sm1.av2.mt0.at0.as0.dv0.sh2.rt13264.rc0.edge.basic.stream/playlist.m3u8'
    },
    {
        'label': 'WhaleShark',
        'id': 'WhaleShark',
        'weight': 0.2,
        'url': 'https://streams.chilaxan.cc/WhaleShark.mp4.m3u8' # 'https://usw01-smr03-relay.ozolio.com/hls-live/_definst_/relay01.hqko7z.fd0.sm1.av2.mt0.at0.as0.dv0.sh2.rt13264.rc0.edge.basic.stream/playlist.m3u8'
    }
]

threads = []

fps = 15
time_delta = 1./fps

def launchStream(stream_url):
    FrameCell = CellType()
    def target():
        #resp = requests.get(streamRelay.format(stream_id)).json()
        vcap = cv2.VideoCapture(stream_url)#resp['output']['source'])
        wt = 1 / fps
        while True:
            start_time = time.time()
            ret, frame = vcap.read()
            if frame is not None:
                ret, buffer = cv2.imencode('.jpg', frame)
                FrameCell.cell_contents = (b'--frame\r\n'
                                b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
                time.sleep(time_delta)
    t = threading.Thread(target=target)
    t.setDaemon(True)
    threads.append(t)
    t.start()
    return FrameCell

streamFrames = {stream['id']: launchStream(stream['url']) for stream in streams}

def makeStream(stream_id):
    frameContainer = streamFrames[stream_id]
    while True:
        try:
            yield frameContainer.cell_contents
            time.sleep(time_delta)
        except ValueError:
            pass
