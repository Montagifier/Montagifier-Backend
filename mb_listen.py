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
        s.wfile.write(util.sounds_json.encode('utf8'))

    def do_POST(s):
        global _courier
        if not _courier:
            s.send_response(500)
            s.end_headers()
            return

        # Parse request
        try:
            length = int(s.headers['Content-Length']) 
            data = s.rfile.read(length).decode('utf-8')
            req = tuple(i.strip() for i in data.split(':'))
        except Exception as e:
            s.send_response(400)
            s.end_headers()
            print(e)
            return

        req_obj = None
        
        if req[0] == 'video':
            req_obj = Video(req[1])
            if not req_obj.duration:
                s.send_response(400)
                s.end_headers()
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
            s.end_headers()
            return

        _courier.put(req_obj)
        s.send_response(202)
        s.end_headers()

def listen(courier, host, port):
    import prctl, signal
    prctl.set_pdeathsig(signal.SIGKILL)

    global _courier
    _courier = courier

    print("Starting HTTP Server...")
    httpd = socketserver.TCPServer((host, port), MobileRequestHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        return

