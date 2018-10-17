#! /usr/bin/env python3
import sys, os, socket, params, time, queue
from threading import *
from frSock import FramedStreamSock

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-d', '--debug'), "debug", True), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)
debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("listening on:", bindAddr)
ClientWait = queue.Queue()  # hashtagMyCode
lock = Lock()
receiving = Condition()  # hashtagMyCode

class ServerThread(Thread):
    requestCount = 0            # one instance / class

    def __init__(self, sock, debug):
        Thread.__init__(self, daemon=True)
        self.fsock, self.debug = FramedStreamSock(sock, debug), debug
        self.start()
        self.join()

    def run(self):
        global available
        while True:
            msg = self.fsock.receivemsg()
            if not msg:
                if self.debug: print(self.fsock, "server thread done")
                return
            requestNum = ServerThread.requestCount
            time.sleep(0.001)
            ServerThread.requestCount = requestNum + 1
            msg = ("%s! (%d)" % (msg, requestNum)).encode()
            self.fsock.sendmsg(msg)


while True:
    sock, addr = lsock.accept()
    ClientWait.put(sock)
    receiving.acquire()
    ServerThread(ClientWait.get(), debug)
    receiving.release()









