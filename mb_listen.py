import http.server
import socketserver
import util
from util import Video, Sound, Skip

_courier = None

class MobileRequestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(s):
        s.send_response(200)
        s.send_header("Content-type", "application/json")
        s.end_headers()
        s.wfile.write(util.sounds_json)

    def do_POST(s):
        global _courier
        if not _courier:
            s.send_response(500)
            return

        # Parse request
        try:
            data = s.rfile.read(s.headers.getheader('content-length'))
            req = tuple(i.strip() for i in data).split(':')
        except Exception as e:
            s.send_response(400)
            print(e.strerr)
            return

        req_obj = None
        
        if req[0] == 'video':
            req_obj = Video(req[1])
            if not req_obj.duration:
                s.send_response(400)
                return
        elif req[0] == 'sound' and utils.search_sounds(req[1], req[2]):
            req_obj = Sound(req[1], req[2])
        elif req[0] == 'skip':
            req_obj = Skip()
        elif req[0] == 'checkin':
            req_obj = CheckIn()
        elif req[0] == 'checkout':
            req_obj = CheckOut()
        else: 
            # Malformed request
            s.send_response(400)
            return

        _courier.put(req_obj)
        s.send_response(202)

def listen(courier, host, port):
    global _courier
    _courier = courier
    print("Starting HTTP Server...")
    httpd = socketserver.TCPServer((host, port), MobileRequestHandler)
    httpd.serve_forever()

