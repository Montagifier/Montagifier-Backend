Montagifier-Backend
===================
Python HTTP and WebSocket Servers

Dependencies
------------

Python 3+

websocket_server Package (https://pypi.python.org/pypi/websocket-server/0.4)

Usage
-----

To run:
`python3 serve.py`

By default, serves on 'localhost' on ports 8080 (HTTP) and 8765 (WS).

Notes
-----

Python 3 has caused a lot of trouble.
- Documentation is fragmented and poor
- Incompatibility between adjacent versions
- Different parts of the standard library are incompatible (asyncio with multiprocessing, for example)

In short, we won't be using Python 3 again for a very very very very long time.
