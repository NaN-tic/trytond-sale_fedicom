# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.

from . import logger
from .messages.close_session import *
from .messages.init_session import *
from .messages.order import *
from .messages.order_line import *
from .messages.finish_order import *
import socket

user = 'user'
password = 'passowrd'

#lin = "9999999:010,9999999:001"
lin = "1127716:010,9123456:0123"


def sendOrder():
    msg = ""
    msg += str(InitSession(user, password, ''))
    msg += str(Order(user, '1'))
    amount = 0
    lines = lin.split(",")
    for line in lines:
        code, qty = line.split(":")
        amount += int(qty)
        msg += str(OrderLine(code, qty))
    f = FinishOrder()
    f.finishOrder(str(len(lines)), qty, 0)
    msg += str(f)
    msg += str(CloseSession())
    return msg

log = logger.Logger()

host = 'localhost'
port = 1234

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))

msg = sendOrder()
sock.sendall(msg)
data = sock.recv(2048)
sock.close()

data_list = data.split('\r\n')

for msg in data_list:
    print(msg)

exit(0)
