# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.

from .message import *


class FinishOrder(Message):
    def __init__(self):
        pass

    def set_msg(self, message):
        self.code = message[0:2]
        self.subcode = message[2:4]
        self.num_lines = message[4:8]
        self.total_amount = message[8:14]
        self.bonus = message[14:20]

    def finishOrder(self, num_lines, total_amount, bonus):
        self.code = message['FINISH_ORDER_CODE']
        self.subcode = message['FINISH_ORDER_SUBCODE']
        self.num_lines = num_lines
        self.total_amount = total_amount
        self.bonus = bonus

    def next_state(self):
        return ['1010', '0199']

    def __str__(self):
        return message['FINISH_ORDER_CODE'] + \
            message['FINISH_ORDER_SUBCODE'] + \
            self.numlines.rjust(4, '0') + \
            self.total_amount.rjust(6, '0') + \
            self.bonus.rjust(6, '0') + \
            message[END_MESSAGE]
