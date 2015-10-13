import time, threading, json
from websocket_server import WebsocketServer
from collections import deque, OrderedDict
from util import Video, Sound, Skip, CheckIn, CheckOut

QUEUE_MAX = 2048 

skip = 0
v_time = 0
playing = False
mb_users = 0
videos = deque()

def next_video(server):
    global v_time, skip, videos, playing
    if len(videos) > 0:
        if playing:
            videos.popleft()

        if len(videos) > 0:
            server.send_message_to_all(str(videos[0]))
    if len(videos) == 0:
        playing = False
    else:
        v_time = 0
        skip = 0
        playing = True

def updater(courier, server):
    global v_time, skip, videos, mb_users, playing
    while True:
        if len(videos) > 0 and (v_time > videos[0].duration or not playing):
            next_video(server)

        req = courier.get()

        try:
            if type(req) is Video and len(videos) < QUEUE_MAX:
                videos.append(req)
            elif type(req) is Sound:
                server.send_message_to_all(str(req))
            elif type(req) is Skip:
                skip += 1
                if skip >= (len(server.clients) + mb_users) / 2:
                    next_video(server)
            elif type(req) is CheckIn:
                mb_users += 1
            elif type(req) is CheckOut:
                if mb_users > 0:
                    mb_users -= 1
        except Exception as e:
            print(e)


def v_timer(server):
    global v_time, videos, playing
    while True:
        print(videos, v_time, playing)
        if len(videos) > 0:
            print(videos[0].__dict__)
        time.sleep(0.2)
        if videos and playing:
            v_time += 0.2

def notify_client(client, server):
    if len(videos) > 0:
        data = videos[0].__dict__
        data['position'] = v_time
        server.send_message(client, json.dumps(data))

def listen(courier, host, port):
    server = WebsocketServer(port)
    server.set_fn_new_client(notify_client)

    uthread = threading.Thread(target=updater, args=(courier, server))
    tthread = threading.Thread(target=v_timer, args=(server,))

    uthread.daemon = True
    tthread.daemon = True

    uthread.start()
    tthread.start()

    print("Starting WebSocket Server...")
    server.run_forever()
    
