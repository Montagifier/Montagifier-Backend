#!/usr/bin/python3

import ws_listen
import mb_listen

from multiprocessing import Process, Queue
from threading import Thread

if __name__ == '__main__':
    courier = Queue()

    mb_server = Thread(target=mb_listen.listen, args=(courier, '', 8080))
    mb_server.start()

    ws_server = Process(target=ws_listen.listen, args=(courier, '', 8765))
    ws_server.start()

    try:
        ws_server.join()
        mb_server.join()
    except KeyboardInterrupt:
        print("Caught keyboard interrupt.")

