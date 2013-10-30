#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.

from message import *


class FreeText(Message):

    def __init__(self, msg):

        self.code = message['FREE_TEXT_CODE']
        self.subcode = message['FREE_TEXT_SUBCODE']
        self.msg = msg

    def msg(self):
        return self.msg

    def setMsg(self, msg):
        self.msg = msg

    def __str__(self):
        return message['FREE_TEXT_CODE'] +\
            message['FREE_TEXT_SUBCODE'] +\
            self.msg.ljust(50) +\
            message['END_MESSAGE']
