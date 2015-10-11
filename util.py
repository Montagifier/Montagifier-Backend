import json
import http.client
from datetime import timedelta
from urllib.request import urlopen
from xml.dom.minidom import parseString

YT_URL = 'https://gdata.youtube.com/feeds/api/videos/{0}?v=2i&alt=jsonc'

class Video:
    def __init__(self, link):
        self.link = link
        try:
            response = urlopen(YT_URL.format(link)).read()
            obj = json.loads(response)
            self.duration = int(obj['duration'])
        except:
            self.duration = 0

    def __str__(self):
        return json.dumps(self.__dict__)

class Sound:
    def __init__(self, category, name):
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
