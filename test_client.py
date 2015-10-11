import http.client
import sys

conn = http.client.HTTPConnection("localhost", 8080)
while True:
    sys.stdout.write("> ")
    i = input()
    cmd = i.split(" ")
    conn.request(cmd[0], '/', body=cmd[1])
    r1 = conn.getresponse()
    print(r1.status, r1.reason)

