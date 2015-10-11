#!/usr/bin/python3

import ws_listen
import mb_listen

from multiprocessing import Process, Queue

if __name__ == '__main__':
    courier = Queue()

    ws_server = Process(target=ws_listen.listen, args=(courier, 'localhost', 8765))
    mb_server = Process(target=mb_listen.listen, args=(courier, 'localhost', 8080))

    ws_server.start()
    mb_server.start()

    ws_server.join()
    mb_server.join()
