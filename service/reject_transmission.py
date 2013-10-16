from message import *
class RejectTransmission( Message ):
    def  __init__( self, msg ):
        self.code = messages['REJECT_TRANSMISSION_CODE']
        self.subcode =  messages['REJECT_TRANSMISSION_SUBCODE']
        self.msg = msg.ljust(50,' ')

    def __str__( self  ):       
        return self.code + self.subcode + self.msg + messages['END_MESSAGE']
