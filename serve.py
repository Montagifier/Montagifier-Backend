#!/usr/bin/python3

import argparse
import ws_listen
import mb_listen
from Queue import Queue

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Montagifier Websocket and HTTP server')
    parser.add_argument('AUDIOPATH', help='Path to audio files')

    args = parser.parse_args()

    courier = Queue()
    mb_listen.listen(courier, '', 8080, args.AUDIOPATH)
    ws_listen.listen(courier, '', 8765)
