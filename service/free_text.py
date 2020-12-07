# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from .message import Message, messages


class FreeText(Message):

    def __init__(self, msg):
        self.code = messages['FREE_TEXT_CODE']
        self.subcode = messages['FREE_TEXT_SUBCODE']
        self.msg = msg

    def msg(self):
        return self.msg

    def setMsg(self, msg):
        self.msg = msg

    def __str__(self):
        return messages['FREE_TEXT_CODE'] + \
            messages['FREE_TEXT_SUBCODE'] + \
            self.msg.ljust(50) + \
            messages['END_MESSAGE']
