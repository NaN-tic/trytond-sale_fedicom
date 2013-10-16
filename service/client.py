# encodine: utf-8
#!/usr/bin/python
##############################################################################
#
# Copyright (c) 2012 NaN Projectes de Programari Lliure, S.L.
#                         All Rights Reserved.
#                         http://www.NaN-tic.com
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################


import logger
from  messages.close_session import *
from  messages.init_session import *
from  messages.order import *
from  messages.order_line import *
from  messages.finish_order import *
import socket

user = 'user'
password = 'passowrd'

#lin = "9999999:010,9999999:001"
lin = "1127716:010,9123456:0123"

def sendOrder():
    msg = ""
    msg += str( InitSession(user, password,''))
    msg += str( Order(user,'1') )
    amount=0
    lines = lin.split(",")
    for line in lines:
        code,qty = line.split(":")
        print code, qty
        amount += int(qty)
        msg += str( OrderLine(code, qty))
    f = FinishOrder()
    f.finishOrder( str(len(lines)), qty, 0)
    msg += str( f )
    msg += str( CloseSession())

    return msg



log = logger.Logger()


host = 'localhost'
port = 60000

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host,port))

msg = sendOrder()
sock.sendall(msg)
data = sock.recv(2048)
sock.close()

data_list = data.split('\r\n')

for msg in data_list:
    print msg

exit(0)



