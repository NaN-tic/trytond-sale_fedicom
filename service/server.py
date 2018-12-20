#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.

import threading
import logger
from clientthread import *

log = logger.Logger()


class ServerThread(threading.Thread):

    def __init__(self, interface, port):
        threading.Thread.__init__(self)
        self.port = port
        self.interface = interface
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.socket.bind((self.interface, self.port))
        self.socket.listen(5)
        self.threads = []

    def run(self):
        try:
            self.running = True
            while self.running:
                log.notifyChannel("server.py", logger.LOG_INFO,
                    'Esperant connexions')
                (clientsocket, address) = self.socket.accept()
                log.notifyChannel("server.py", logger.LOG_INFO,
                    'Entrant un nou client %s, %s' % (clientsocket, address))
                ct = ClientThread(clientsocket, self.threads)
                log.notifyChannel("server.py", logger.LOG_INFO, 'Thread creat')
                self.threads.append(ct)
                ct.start()
                log.notifyChannel("server.py", logger.LOG_INFO,
                    'Thread iniciat')
        except Exception as e:
            e.printstack()
            log.notifyChannel("server.py", logger.LOG_CRITICAL,
                'Excepcion entrant un client %s' % e)
        self.socket.close()
        return False

    def stop(self):
        self.running = False
        for t in self.threads:
            t.stop()
            try:
                if hasattr(socket, 'SHUT_RDWR'):
                    self.socket.shutdown(SHUT_RDWR)
                else:
                    self.socket.shutdown(2)
                    self.socket.close()
            except:
                return False
