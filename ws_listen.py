import asyncio
import websockets
import time
import threading
from asyncio import Queue
from collections import deque, OrderedDict
from util import Video, Sound, Skip, CheckIn, CheckOut

CONN_MAX = 2048 
QUEUE_MAX = 2048 

class State:
    courier = None
    connections = OrderedDict()
    skip = 0
    time = 0
    mb_users = 0
    videos = deque()

    @classmethod
    def register(cls, websocket):
        if len(cls.connections) > CONN_MAX:
            websocket.close()
            return False
        cls.connections[websocket] = Queue()
        return True

    @classmethod
    def unregister(cls, websocket):
        del cls.connections[websocket]

    @classmethod
    def broadcast(cls, msg):
        for conn, queue in cls.connections.items():
            queue.put(msg)

    @classmethod
    def next_video(cls):
        if cls.videos:
            cls.videos.popleft()
            cls.broadcast(cls.videos[0])
        cls.time = 0
        cls.skip = 0

@asyncio.coroutine
def handler(websocket, path):
    if State.videos:
        yield from websocket.send(str(State.videos[0]))
    if State.register(websocket):
        while True:
            update = yield from State.connections[websocket].get()

            if type(update) in (Video, Sound):
                yield from websocket.send(str(update))

            if not websocket.open:
                break
        State.unregister(websocket)

def updater():
    while True:
        if State.videos and State.time > State.videos[0].duration:
            State.next_video()

        req = None
        if not State.courier.empty():
            req = State.courier.get(block=False)
        else:
            continue

        if type(req) is Video and len(State.videos) < QUEUE_MAX:
            State.videos.append(req)
        elif type(req) is Sound:
            State.broadcast(req)
        elif type(req) is Skip:
            State.skip += 1
            if State.skip > (len(State.connections) + State.mb_users) / 2:
                State.next_video()
        elif type(req) is CheckIn:
            State.mb_users += 1
        elif type(req) is CheckOut:
            State.mb_users -= 1

        time.sleep(1)
        State.time += 1

def listen(courier, host, port):
    import prctl, signal
    prctl.set_pdeathsig(signal.SIGKILL)

    State.courier = courier
    uthread = threading.Thread(target=updater, daemon=True)
    uthread.start()

    print("Starting WebSocket Server...")
    start_server = websockets.serve(handler, host, port)
    try:
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        return

    uthread.join()

