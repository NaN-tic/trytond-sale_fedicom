#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.

from message import *


class RejectTransmission(Message):
    def __init__(self, msg):
        self.code = messages['REJECT_TRANSMISSION_CODE']
        self.subcode = messages['REJECT_TRANSMISSION_SUBCODE']
        self.msg = msg.ljust(50, ' ')

    def __str__(self):
        return self.code + self.subcode + \
            self.msg + messages['END_MESSAGE']
