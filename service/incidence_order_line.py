# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.

from message import *


class IncidenceOrderLine(Message):

    def __init__(self, article_code=None, amount=None,
          not_served=None, code=None):

        self.code = messages['INCIDENCE_ORDER_LINE_CODE']
        self.subcode = messages['INCIDENCE_ORDER_LINE_SUBCODE']
        self.article_code = str(article_code)
        self.amount = str(amount)
        self.amount_not_served = str(not_served)
        self.bonus = ''
        self.bonus_not_served = ''
        self.incidence_code = str(code)
        self.article_alternative = ''
        self.incidences = {
          'NOT_STOCK': '01',
          'NOT_SERVE': '02',
          'NOT_WORKED': '03',
          'UNKNOWN': '04',
          'DRUG': '05',
          'TO_ORDER': '06',
          'TO_DROP_OUT': '07',
          'PASS_TO_WAREHOUSE': '08',
          'NEW_SPECIALITY': '09',
          'TEMPORAL_DROP_OUT': '10',
          'DROP_OUT': '11',
          'TO_ORDER_OK': '12',
          'LIMIT_SERVICE': '13',
          'SANITY_REMOVED': '14'
        }

    def set_order_line(self, orderline):
        self.article_code = orderline.article_code
        self.amount = orderline.amount
        self.amount_not_served = orderline.amount_not_served
        self.incidence_code = orderline.incidence_type

    def __str__(self):
        return messages['INCIDENCE_ORDER_LINE_CODE'] + \
               messages['INCIDENCE_ORDER_LINE_SUBCODE'] + \
               self.article_code + \
               self.amount.rjust(4, '0') + \
               self.amount_not_served.rjust(4, '0') + \
               self.bonus.rjust(4, '0') + \
               self.bonus_not_served.rjust(4, '0') + \
               self.incidences[self.incidence_code] + \
               self.article_alternative.rjust(13, '0') +\
               messages['END_MESSAGE']
