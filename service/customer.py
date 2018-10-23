# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.

from .order import Order


class Customer:
    def __init__(self, user_code='', password=''):
        self.user_code = user_code[2, 8]
        self.user = user_code
        self.password = password
        self.order = []
        self.date = None

    def set_message(self, init_session):
        self.user_code = init_session.user_code[2, 8]
        self.user = init_session.user_code
        self.password = init_session.password
        self.date = init_session.date

    def add_order(self, order_msg):
        self.order.append(Order(order_msg))

    def last_order(self):
        self.order[-1]

    def check(self, user, passwd):
       # No necessari, rpc s'encarrega de tot
        pass

    def process_order(self):
        # No necessari, rpc fa
        pass

    def incidence(self):
        # de moment no...
        pass
