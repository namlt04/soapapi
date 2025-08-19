
from spyne import Boolean, Unicode, ComplexModel, Int

class CreateAccountRequest(ComplexModel): 
    id_customer = Unicode
    number_account = Unicode 
    session_key = Unicode 


class CreateAccountResponse(ComplexModel): 
    status = Boolean
    number_account = Unicode 
    balance_account = Int
    message = Unicode
class ChangeStatusAccountRequest(ComplexModel): 
    id_customer = Unicode 
    number_account = Unicode 
    type = Int
    session_key = Unicode
    dotp = Unicode

class ChangeStatusAccountReponse(ComplexModel): 
    status = Boolean
    message = Unicode

