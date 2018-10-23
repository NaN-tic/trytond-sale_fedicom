# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.

from .message import *


class IncidenceHeader(Message):

    def __init__(self, user_code, order_number):
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
               self.get_date_send_order() + \
               self.get_day_send_order() + \
               self.get_error_totals() + \
               self.msg.ljust(30, ' ') + \
               messages['END_MESSAGE']
