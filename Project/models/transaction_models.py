
from spyne import Boolean, Int, Unicode, ComplexModel


class BankTransferRequest(ComplexModel):
    number_account_send = Unicode
    bank_name_send = Unicode
    number_account_receive= Unicode
    bank_name_receive = Unicode
    session_key = Unicode 
    value =Int
    d_otp = Unicode 
    content = Unicode 



class BankTransferResponse(ComplexModel):
    status = Boolean
    bank_name_send = Unicode
    number_account_receive= Unicode
    bank_name_receive = Unicode
    session_key = Unicode 
    d_otp = Unicode 
    content = Unicode 
    message = Unicode
