#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.

from message import *


class IncidenceHeader(Message):

    def __init__(self, user_code='', order_number=''):
        self.code = messages["INCIDENCE_HEADER_CODE"]
        self.subcode = messages['INCIDENCE_HEADER_SUBCODE']
        self.user_code = user_code
        self.order_number = order_number
        self.order_rejected = False
        self.type = False
        self.condition_service = False
        self.charge_cooperative = False
        self.charge_deferment = False
        self.pay_deferment = False
        self.additional_charge = False
        self.enterprise = False
        self.warehouse = False
        self.date_send_order = False
        self.day_send_order = False
        self.error_totals = False
        self.msg = ''

    def get_error_totals(self):
        if self.error_totals:
            return '1'
        else:
            return '0'

    def get_day_send_order(self):
        if self.day_send_order:
            return '1'
        else:
            return '0'

    def get_date_send_order(self):
        if self.date_send_order:
            return '1'
        else:
            return '0'

    def get_enterprise(self):
        if self.charge_cooperative:
            return '1'
        else:
            return '0'

    def get_additional_charge(self):
        if self.additional_charge:
            return '1'
        else:
            return '0'

    def get_pay_deferement(self):
        if self.pay_deferment:
            return '1'
        else:
            return '0'

    def get_warehouse(self):
        if self.warehouse:
            return '1'
        else:
            return '0'

    def get_charge_cooperative(self):
        if self.charge_cooperative:
            return '1'
        else:
            return '0'

    def get_charge_deferement(self):
        if self.charge_deferment:
            return '1'
        else:
            return '0'

    def get_condition_service(self):
        if self.condition_service:
            return '1'
        else:
            return '0'

    def get_type(self):
        if self.type:
            return '1'
        else:
            return '0'

    def get_order_rejected(self):
        if self.order_rejected:
            return '1'
        else:
            return '0'

    def set_msg(self, msg):
        self.code = msg[0:2]
        self.subcode = msg[2:4]
        self.user_code = msg[4:20].strip()
        self.order_number = msg[20:30].strip()
        self.order_rejected = msg[30:31]
        self.type = msg[31:32]
        self.condition_service = msg[32:33]
        self.charge_cooperative = msg[33:34]
        self.charge_deferment = msg[34:35]
        self.pay_deferment = msg[35:36]
        self.additional_charge = msg[36:37]
        self.enterprise = msg[37:38]
        self.warehouse = msg[38:39]
        self.date_send_order = msg[39:40]
        self.day_send_order = msg[40:41]
        self.error_totals = msg[41:42]
        self.msg = msg[42:72].strip()

    def __str__(self):
        return messages['INCIDENCE_HEADER_CODE'] +  \
               messages['INCIDENCE_HEADER_SUBCODE'] + \
               self.user_code.ljust(16, ' ') + \
               self.order_number.ljust(10, ' ') + \
               self.get_order_rejected() + \
               self.get_type() + \
               self.get_condition_service() + \
               self.get_charge_cooperative() + \
               self.get_charge_deferement() +  \
               self.get_pay_deferement() +  \
               self.get_additional_charge() + \
               self.get_enterprise() +  \
               self.get_warehouse() + \
               self.get_date_send_order() +  \
               self.get_day_send_order() +   \
               self.get_error_totals() +  \
               self.msg.ljust(30, ' ') + \
               messages['END_MESSAGE']

    def next_state(self):
        return ['2011', '2015', '2016', '0199']
