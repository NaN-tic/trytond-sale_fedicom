# encoding: utf-8
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import os
import threading
from _socket import *
from . import logger
from .nan_socket import *
from .messages.init_session import InitSession
from .messages.close_session import CloseSession
from .messages.finish_order import FinishOrder
from .messages.incidence_header import IncidenceHeader
from .messages.incidence_order_line import IncidenceOrderLine
from .messages.order_line import OrderLine
from .messages.order import Order
from .messages.reject_transmission import RejectTransmission

from trytond.config import config, parse_uri
config.update_etc(os.environ.get('TRYTOND_CONFIG'))
from trytond.transaction import Transaction
from trytond.pool import Pool

FEDICOM_USER = config.getint('fedicom', 'user', default=1)


log = logger.Logger()


class ClientThread(threading.Thread):

    def __init__(self, sock, threads):
        threading.Thread.__init__(self)
        self.socket = sock
        self.threads = threads
        self.user = None
        self.password = None
        self.date = None
        self.ts = None

        self.article = {}

    def run(self):
        self.running = True
        try:
            self.ts = Socket(self.socket)
        except Exception as e:
            log.notifyChannel("clientthread.py", logger.LOG_CRITICAL,
                'Error obrint el socket, %s' % (e))
            self.socket.close()
            self.threads.remove(self)
            return False

        while self.running:
            try:
                print("Esperant dades en el client")
                msg = self.ts.recieve()
                self.running = False
                print("rebut", msg)
                break
            except Exception as e:
                log.notifyChannel("clientthread.py", logger.LOG_CRITICAL,
                    'Error al rebre les dades, %s' % (e))
                self.socket.close()
                self.threads.remove(self)
                return False
        print("processant el missatge")
        # Es pot rebre None per algun error en la recepció o perquè no s'ha
        #rebut res en acabat el timeout
        if msg is None:
            log.notifyChannel("clientthread.py", logger.LOG_CRITICAL,
                "No s'han rebut dades. Tancant el socket.")
            self.socket.close()
            self.threads.remove(self)
            return False

        self.process_message(msg)
        self.ts.disconnect()
        self.socket.close()
        self.threads.remove(self)
        return True

    def stop(self):
        self.running = False

    def process_message(self, msg):

        msg_list = msg.split('\r\n')
        i = 0

        log.notifyChannel("clientthread.py", logger.LOG_INFO, 'Processant '
            'Init Session Message, %s' % (msg_list[i]))
        init_session = InitSession()
        init_session.set_message(msg_list[i])

        customer_code = self.user = init_session.user_code
        password = self.password = init_session.password
        self.date = init_session.date

        i = i + 1
        next_message = init_session.next_state()
        order = {}
        orderlines = {}
        while i < len(msg_list) - 1:
            log.notifyChannel("clientthread.py", logger.LOG_INFO, 'Processant'
                ' Message, %s' % (msg_list[i]))
            msg = msg_list[i]
            if not msg[0:4] in next_message:
                log.notifyChannel("clientthread.py", logger.LOG_CRITICAL,
                    'Estat no reconegut, estat %s dels possibles %s'
                    % (msg[0:4], str(next_message)))
                reject_transmission = RejectTransmission("Se ha producido un "
                    "error, Trama enviada no pertenece al estado siguiente")
                self.ts.send(str(reject_transmission))
                break

            for state in next_message:
                if msg.startswith(state):
                    if msg.startswith('0199'):  # Close Session
                        log.notifyChannel("clientthread.py", logger.LOG_INFO,
                            'Processant Tancament de Sessio')
                        next_message = None
                        self.process_order(customer_code, password, order)
                        return
                    elif msg.startswith('1010'):  # capsalera comanda
                        orderlines = {}
                        log.notifyChannel("clientthread.py", logger.LOG_INFO,
                            'Processant capsalera comanda')
                        o = Order()
                        o.set_msg(msg)
                        next_message = o.next_state()
                    elif msg.startswith('1020'):
                        log.notifyChannel("clientthread.py", logger.LOG_INFO,
                            'Processant  Linia Comanda')
                        order_line = OrderLine()
                        order_line.set_msg(msg)
                        next_message = order_line.next_state()
                        orderlines[order_line.article_code] = \
                            int(order_line.amount)
                        self.article[order_line.article_code] = \
                            order_line.article_code

                    elif msg.startswith('1050'):
                        log.notifyChannel("clientthread.py", logger.LOG_INFO,
                            'Processant  final  Comanda')
                        finish_order = FinishOrder()
                        finish_order.set_msg(msg)
                        next_message = finish_order.next_state()
                        order[o.order_number] = orderlines
                    else:
                        log.notifyChannel("clientthread.py", logger.LOG_INFO,
                            'Tram no tractada.')
                        reject_transmission = RejectTransmission("Se ha "
                            "producido un error, Trama enviada no reconocida")
                        self.ts.send(str(reject_transmission))
                        return

            i = i + 1
        return

    def to_send_order_lines(self, orderlines):
        lines = []
        for k, v in orderlines.items():
            lines.append((k, v))
        return lines

    def process_order(self, user, password, orders):
        log.notifyChannel("clientthread.py", logger.LOG_INFO, "1")

        uri = parse_uri(config.get('database', 'uri'))
        dbname = uri.path[1:]
        if dbname:
            log.notifyChannel("clientthread.py", logger.LOG_INFO,
                'Database: %s' % dbname)
        else:
            log.notifyChannel("clientthread.py", logger.LOG_ERROR, 'Not found '
                'trytond.conf file in TRYTOND_CONFIG env or empty database uri')
            return

        Pool.start()
        pool = Pool(dbname)
        pool.init()

        send = {}
        context = {'active_test': False}
        with Transaction().start(dbname, FEDICOM_USER, context=context):
            Sale = pool.get('sale.sale')

            for order in orders:
                orders_to_send = self.to_send_order_lines(orders[order])
                result = Sale.process_order([], user.strip(), password.strip(),
                    order, orders_to_send)
                log.notifyChannel("clientthread.py", logger.LOG_INFO, 'Comanda '
                       'Processada, generant resposta... %s' % result)
                misses = []
                current_order = orders[order]
                reject_transmission = None
                if result.get('error', False):
                    log.notifyChannel("clientthread.py", logger.LOG_INFO,
                       result['error'])
                    reject_transmission = RejectTransmission(result['error'])
                else:
                    for miss in result['missingStock']:
                        (article, not_served, reason) = miss
                        amount = current_order[article]
                        log.notifyChannel("clientthread.py", logger.LOG_INFO,
                            "Comanda %s, Article %s, Demanat:%s, No Servit %s, "
                            "Rao:%s " % (str(order), str(article),
                                str(int(amount)), str(int(not_served)),
                                str(reason)))
                        iline = IncidenceOrderLine(self.article[article],
                            int(amount), int(not_served), reason)
                        misses.append(iline)

                send[order] = {}
                send[order]['order'] = orders[order]
                send[order]['misses'] = misses
                if reject_transmission is not None:
                    send[order]['error'] = reject_transmission

            self.send_data(send)

    def send_data(self, send_data):
        result = str(InitSession(self.user, self.password, self.date))
        for k, order in send_data.items():
            if order.get('error', False):
                self.ts.send(str(order['error']) + str(CloseSession("")))
                return
            result += str(IncidenceHeader(self.user, k))
            order['order']
            for miss in order['misses']:
                result += str(miss)
        result += str(CloseSession(""))
        log.notifyChannel("clientthread.py", logger.LOG_INFO,
            "Resposta:%s" % result.replace("\r\n", "<lf><cr>\r\n"))
        self.ts.send(result)
