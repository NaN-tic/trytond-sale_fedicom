# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.


class Message:
    def __init__(self, code, subcode):
        self.code = code
        self.subcode = subcode

messages = {
    'CLOSE_SESSION_CODE': "01",
    'CLOSE_SESSION_SUBCODE': '99',
    'CLOSE_SESSION_LENGTH_MESSAGE': 6,
    'END_MESSAGE': '\r\n',
    'FINISH_ORDER_CODE': '10',
    'FINISH_ORDER_SUBCODE': '50',
    'FREE_TEXT_CODE': '20',
    'FREE_TEXT_SUBCODE': '11',
    'INCIDENCE_HEADER_CODE': '20',
    'INCIDENCE_HEADER_SUBCODE': '10',
    'INCIDENCE_ORDER_LINE_CODE': '20',
    'INCIDENCE_ORDER_LINE_SUBCODE': '15',
    'INIT_SESSION_CODE': '01',
    'INIT_SESSION_SUBCODE': '01',
    'INIT_SESSION_LENGHT:': 44,
    'ORDER_LINE_CODE': '10',
    'ORDER_LINE_SUBCODE': '20',
    'ORDER_LINE_PLUS_CODE': '10',
    'ORDER_LINE_PLUS_SUBCODE': '30',
    'ORDER_CODE': '10',
    'ORDER_SUB_CODE': '10',
    'FIXED_LENGTH': 66,
    'REJECT_TRANSMISSION_CODE': '99',
    'REJECT_TRANSMISSION_SUBCODE': '99'
}
