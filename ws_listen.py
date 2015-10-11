import time, queue, threading
from websocket_server import WebsocketServer
from socketserver import ThreadingMixIn, TCPServer
from collections import deque, OrderedDict
from util import Video, Sound, Skip, CheckIn, CheckOut

QUEUE_MAX = 2048 

skip = 0
v_time = 0
mb_users = 0
videos = deque()

def next_video(server):
    global v_time, skip, videos
    if videos:
        videos.popleft()
        server.send_message_to_all(str(videos[0]))
    v_time = 0
    skip = 0

def updater(courier, server):
    global v_time, skip, videos, mb_users
    while True:
        if videos and v_time > videos[0].duration:
            next_video(server)

        req = courier.get()

        if type(req) is Video and len(videos) < QUEUE_MAX:
            videos.append(req)
        elif type(req) is Sound:
            server.send_message_to_all(str(req))
        elif type(req) is Skip:
            skip += 1
            if skip > (len(server.clients) + mb_users) / 2:
                next_video(server)
        elif type(req) is CheckIn:
            mb_users += 1
        elif type(req) is CheckOut:
            if mb_users > 0:
                mb_users -= 1


def v_timer(server):
    global v_time, videos
    while True:
        if videos:
            time.sleep(1)
            v_time += 1


def listen(courier, host, port):
    import prctl, signal
    prctl.set_pdeathsig(signal.SIGKILL)

    server = WebsocketServer(port)

    uthread = threading.Thread(target=updater, args=(courier, server), daemon=True)
    tthread = threading.Thread(target=v_timer, args=(server,), daemon=True)

    uthread.start()
    tthread.start()

    print("Starting WebSocket Server...")
    server.run_forever()
    
