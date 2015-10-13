import util
import threading
from util import Video, Sound, Skip, CheckIn, CheckOut
from flask import Flask, request

_courier = None

def listen(courier, host, port, audiopath):
    global _courier
    _courier = courier

    print("Starting HTTP Server...")
    app = Flask(__name__)

    @app.route('/', methods=['GET'])
    def get_handler():
        data = util.sounds_json.encode('utf8')
        return (data, 200, {'Content-type': 'application/json'})

    @app.route('/', methods=['POST'])
    def post_handler():
        global _courier
        if not _courier:
            return ('', 500)

        # Parse request
        try:
            data = request.get_data().decode('utf8')
            req = tuple(i.strip() for i in data.split(':'))
        except Exception as e:
            print(e)
            return ('', 400)

        req_obj = None
        
        if req[0] == 'video' and len(req) >= 2:
            req_obj = Video(req[1])
            if not req_obj.duration:
                return ('', 400)
        elif req[0] == 'sound' and len(req) >= 3 and util.search_sounds(req[1], req[2]):
            req_obj = Sound(req[1], req[2])
        elif req[0] == 'skip':
            req_obj = Skip()
        elif req[0] == 'checkin':
            req_obj = CheckIn()
        elif req[0] == 'checkout':
            req_obj = CheckOut()
        else: 
            # Malformed request
            return ('', 400)

        _courier.put(req_obj)
        return ('', 202)

    t = threading.Thread(target=app.run, kwargs={'host': host, 'port': port})
    t.daemon = True
    t.start()

