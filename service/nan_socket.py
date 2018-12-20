# -*- encoding: utf-8 -*-
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms

from socket import *
import logger
from messages.close_session import *


log = logger.Logger()


class Socket:

    def __init__(self, sock=None):
        if sock is None:
            self.socket = socket(AF_INET, SOCK_STREAM)
        else:
            self.socket = sock
            self.socket.settimeout(120)

    def connect(self, host='localhost', port=5000):
        self.socket.connect(host, port)

    def disconnect(self):
        self.socket.shutdown(SHUT_RDWR)
        self.socket.close()

    def send(self, msg, exception=False, traceback=None):
        self.socket.sendall(msg)

    def recieve(self):
        try:
            data = ''
            ch = self.socket.recv(1)
            data += ch
            close = str(CloseSession())
            while True:
                print("Esperant recepcio al socket")
                ch = self.socket.recv(1)
                # When len(ch) == 0 it means the other end has
                # closed the socket
                if len(ch) == 0:
                    log.notifyChannel("nan_socket.py",
                        logger.LOG_INFO,
                        "L'altre extrem ha tancat la connexio. "
                        "La informacio acumulada fins al moment era: '%s'" %
                         data)
                    return None
                print("rebuda info al socket")
                data += ch
                log.notifyChannel("nan_socket.py",
                    logger.LOG_DEBUG,
                    'Rebent les dades : %s :=> %s ' % (ch, data))
                if data[len(data)-len(close):] == close:
                    print("Acabat de rebre")
                    break

        except Exception as e:
            log.notifyChannel("nan_socket.py", logger.LOG_ERROR,
                'Error rebent les dades, %s ' % e)
            return None

        log.notifyChannel("nan_socket.py", logger.LOG_DEBUG,
            'Dades Rebudes %s' % data)

        return data
