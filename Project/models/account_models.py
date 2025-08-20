
from spyne import Boolean, Unicode, ComplexModel, Int, Array

class NumberAccount(ComplexModel):
    number_account = Unicode
    balance_account = Int 
    status_account = Unicode 

class CreateAccountRequest(ComplexModel): 
    id_customer = Unicode
    dotp = Unicode
    number_account = Unicode 
    session_key = Unicode 

class CreateAccountResponse(ComplexModel): 
    status = Boolean
    number_account = Unicode 
    balance_account = Int
    message = Unicode


class ListNumberAccountRequest(ComplexModel):
   username = Unicode 
   session_key = Unicode  
class ListNumberAccountResponse(ComplexModel):
    status = Boolean 
    message = Unicode 
    account = Array(NumberAccount)

class ChangeStatusAccountRequest(ComplexModel): 
    id_customer = Unicode 
    number_account = Unicode 
    type = Int
    session_key = Unicode
    dotp = Unicode
class ChangeStatusAccountReponse(ComplexModel): 
    status = Boolean
    message = Unicode

