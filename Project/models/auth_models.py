

from spyne import Unicode, Int, ComplexModel, Boolean

class LoginRequest(ComplexModel): 
    username = Unicode  # Tra id_customer
    password = Unicode 

class LoginResponse(ComplexModel):
    status = Boolean 
    message = Unicode
    id_customer = Unicode
    fullname = Unicode 
    phone = Unicode 
    session_key = Unicode

class RegisterRequest(ComplexModel):
    phone = Unicode 
    fullname = Unicode
    id_customer = Unicode
    password = Unicode
    email = Unicode

class RegisterResponse(ComplexModel): 
    status = Boolean 
    message = Unicode 

class RegisterDOtpRequest(ComplexModel):
    id_customer = Unicode
    dotp = Unicode
    session_key = Unicode

class RegisterDOtpResponse(ComplexModel):
    status = Boolean
    message = Unicode


# class ChangePasswordRequest(ComplexModel): 


# class ChangePassowrdResponse(ComplexModel):
    