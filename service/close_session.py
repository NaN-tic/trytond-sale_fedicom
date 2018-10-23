# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.

from .message import *


class CloseSession(Message):
    def __init__(self, message=None):
        if message:
            self.code = message[0:2]
            self.subcode = message[2:4]
        else:
            self.code = messages['CLOSE_SESSION_CODE']
            self.subcode = messages['CLOSE_SESSION_SUBCODE']

    def check(self):
        if self.code != messages['CLOSE_SESSION_CODE']:
            return False
        if self.subcode != messages['CLOSE_SESSION_SUBCODE']:
            return False
        return True

    def length(self):
        return messages['CLOSE_SESSION_LENGTH_MESSAGE']

    def __str__(self, *args):
        return messages['CLOSE_SESSION_CODE'] + \
            messages['CLOSE_SESSION_SUBCODE'] + \
            messages['END_MESSAGE']
