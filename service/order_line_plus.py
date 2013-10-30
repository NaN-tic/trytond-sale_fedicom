#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.

from message import *


class OrderLinePlus(Message):

    def __init__(self, article_national_code=None, amount=None,
        bonus=None, line_discount=None):

        self.code = messages['ORDER_LINE_PLUS_CODE']
        self.subcode = messages['ORDER_LINE_PLUS_SUBCODE']
        self.bonus = bonus
        self.line_discount = line_discount
        self.article_national_code = article_national_code.rjust(12, '0') + "1"
        self.amount = amount

    def setMsg(self, msg):

        self.code = msg[0:2]
        self.subcode = msg[2:4]
        self.article_code = msg[4:17]
        self.article_national_code = msg[10:16]
        self.amount = int(msg[17:21])
        self.dc = int(msg[21:22])
        self.bonus = int(msg[22:26])
        self.discount = float(msg[26:30])/100

    def __str__(self):
        return self.messages['ORDER_LINE_PLUS_CODE'] +\
            self.messages['ORDER_LINE_PLUS_SUBCODE'] +\
            self.article_code + \
            self.bunus.rjust(4, '0') + \
            str(self.discount).rjust(4, '0') + \
            self.messages['END_MESSAGE']
