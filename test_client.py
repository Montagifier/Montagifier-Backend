import http.client
import sys
import asyncio
import websockets

@asyncio.coroutine
def test():
    websocket = yield from websockets.connect('ws://localhost:8765/')
    while True:
        try:
            msg = yield from websocket.recv()
            if msg is None:
                break
            print(msg)
        except KeyboardInterrupt:
            break
    yield from websocket.close()

if len(sys.argv) >= 2 and sys.argv[1] == '-http':
    conn = http.client.HTTPConnection("localhost", 8080)
    while True:
        cmd = input("> ")
        cmd = cmd.split(" ")
        if cmd[0] == "q":
            break
        conn.request(cmd[0], '/', body=cmd[1])
        r1 = conn.getresponse()
        print(r1.status, r1.reason)
    conn.close()
else:
    asyncio.get_event_loop().run_until_complete(test())
    
