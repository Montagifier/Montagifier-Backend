import json
import http.client
from datetime import timedelta
from urllib.request import urlopen
from xml.dom.minidom import parseString

YT_URL = "https://www.googleapis.com/youtube/v3/videos?id={0}&key={1}&part=contentDetails" 

with open('yt_key', 'r') as f:
    YT_KEY = f.read()

class Video:
    def __init__(self, link):
        self.kind = 'video'
        self.link = link
        try:
            print(YT_URL.format(link, YT_KEY))
            response = urlopen(YT_URL.format(link, YT_KEY)).read()
            print(response)
            obj = json.loads(response)
            self.duration = int(obj['videos'][1]['contentDetails'])
        except Exception as e:
            self.duration = 0
            print("Youtube Error: " + str(e))

    def __str__(self):
        return json.dumps(self.__dict__)

class Sound:
    def __init__(self, category, name):
        self.kind = 'sound'
        self.category = category
        self.name = name

    def __str__(self):
        return json.dumps(self.__dict__)

class Skip:
    pass

class CheckIn:
    pass

class CheckOut:
    pass

sounds = { 
            "Vaporwave" : ["Japanese", "420", "VHS"],
            "Montage"   : ["Noscope", "Clip", "Darude"]
         }

sounds_json = json.dumps(sounds)

def search_sounds(category, name):
    for s in sounds[category]:
        if s == name:
            return True
    return False
