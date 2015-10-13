import json
import requests
import urlparse
import os
from datetime import timedelta
from xml.dom.minidom import parseString

YT_URL = "https://www.youtube.com/get_video_info?video_id={0}"

class Video(object):
    def __init__(self, link):
        self.kind = 'video'
        self.link = link
        try:
            print(YT_URL.format(link))
            response = requests.get(YT_URL.format(link))

            obj = {}
            for k, v in urlparse.parse_qsl(response.text):
                obj[k] = v
            self.duration = int(obj['length_seconds'])
        except Exception as e:
            self.duration = 0
            print("Youtube Error: " + str(e))

    def __str__(self):
        return json.dumps(self.__dict__)

class Sound(object):
    def __init__(self, category, name):
        self.kind = 'sound'
        self.category = category
        self.name = name

    def __str__(self):
        return json.dumps(self.__dict__)

class Skip(object):
    pass

class CheckIn(object):
    pass

class CheckOut(object):
    pass

def get_sounds(audiopath):
    sounds = {}
    for category in os.listdir(audiopath):
        category_path = os.path.join(audiopath, category)
        if os.path.isdir(category_path):
            tracks = []
            for fname in os.listdir(category_path):
                fpath = os.path.join(category_path, fname)
                if os.path.isfile(fpath) and fpath.endswith('.mp3'):
                    tracks.append(fname.rsplit('.')[0])

            sounds[category] = tracks

    return sounds

def search_sounds(audiopath, category, name):
    sounds = get_sounds(audiopath)
    for s in sounds[category]:
        if s == name:
            return True
    return False
