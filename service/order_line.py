#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.

from message import *


class OrderLine(Message):

    def __init__(self, article_code=None, amount=None):
        self.next_message = [
            '1020',  # OrderLine
            '1030',  # OrderLineBonus
            '1050'  # OrderClose
            ]
        self.code = messages['ORDER_LINE_CODE']
        self.subcode = messages['ORDER_LINE_SUBCODE']
        self.article_code = article_code
        self.amount = amount
        self.skip = False
        self.article_national_code = None

    def next_state(self):
        return self.next_message

    def skip(self):
        return self.skip

    def set_msg(self, msg):
        self.code = msg[0:2]
        self.subcode = msg[2:4]
        self.article_code = msg[4:17]
        self.article_national_code = msg[10:16]
        #control digit
        self.amount = msg[17:21]

    def __str__(self):
        return messages['ORDERLINE_CODE'] +\
            messages['ORDERLINE_SUBCODE'] +\
            self.article_code + \
            str(self.amount).rjust(4, '0') +\
            messages['END_MESSAGE']
