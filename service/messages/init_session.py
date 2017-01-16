#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.

from message import *


class InitSession(Message):

    def __init__(self, usercode='', password=None, date=None):
        self.next_message = [
            '1010',  # OrderHeader
            '2010',  # IncidenceHeader
            '0199'   # CloseSession
        ]
        self.code = messages['INIT_SESSION_CODE']
        self.subcode = messages['INIT_SESSION_SUBCODE']
        self.user_code = usercode.rjust(16, ' ')
        self.password = password
        self.date = date

    def set_message(self, message):
        self.code = message[0:2]
        self.subcode = message[2:4]
        self.user_code = message[18:34]
        self.password = message[34:42]
        self.date = message[4:18]

    def check(self):
        if self.code != messages['INIT_SESSION_CODE']:
            return False
        if self.subcode != messages['INIT_SESSION_SUBCODE']:
            return False
        if len(self.user_code) != 16:
            return False
        if len(self.password) != 8:
            return False

        return True

    def length(self):
        return messages['INIT_SESSION_LENGTH']

    def __str__(self):
        return messages['INIT_SESSION_CODE'] +\
            messages['INIT_SESSION_SUBCODE'] +\
            self.date.rjust(14, ' ') +\
            self.user_code.rjust(16, ' ') +\
            self.password.rjust(8, ' ') +\
            messages['END_MESSAGE']

    def next_state(self):
        return self.next_message
