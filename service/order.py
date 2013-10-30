# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.

from message import *


class Order(Message):
    def __init__(self, user_code='', order_number='', order_type='',
      enterprise=''):

        self.code = messages['ORDER_CODE']
        self.subcode = messages['ORDER_SUB_CODE']
        self.user_code = user_code
        self.order_number = order_number,
        self.order_type = order_type,
        self.condition = ""
        self.charge = 0
        self.charge_deferment = 0
        self.pay_deferment = 0
        self.additional_charge = 0
        self.enterprise = enterprise
        self.warehouse = ""
        self.date_send_order = ''
        self.day_send_order = ""

    def set_msg(self, msg):
        self.code = msg[0:2]
        self.subcode = msg[2:4]
        self.user_code = msg[4:20].strip()
        self.order_number = msg[20:30].strip()
        self.order_type = msg[20:36].strip()
        self.condition = msg[36:42].strip()
        self.charge = int(msg[42:43].strip())
        self.charge_deferment = int(msg[43:46].strip())
        self.enterprise = msg[53:56].strip()
        self.warehouse = msg[56:60]
        self.date_send_order = ''
        self.day_send_order = msg[68:70].strip()

    def __str__(self):
        return messages['ORDER_CODE'] + \
               messages['ORDER_SUB_CODE'] + \
               self.user_code.ljust(16, ' ') + \
               self.order_number.ljust(10, ' ') +\
               self.order_type.ljust(6, ' ') + \
               self.condition.ljust(6, ' ') + \
               str(self.charge) + \
               str(self.charge_deferment).rjust(3, '0') + \
               str(self.pay_deferment).rjust(3, '0') + \
               '0000' + \
               self.enterprise.ljust(3, ' ') + \
               self.warehouse.ljust(4, ' ') + \
               str(self.date_send_order) + \
               self.day_send_order + \
               ' ' +\
               messages['END_MESSAGE']

    def length(self):
        return messages['FIXED_LENGHT']

    def check(self):
        return True

    def next_state(self):
        return ['1020', '1030', '1050']
