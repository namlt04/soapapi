
import bcrypt
from spyne import ServiceBase, Unicode, Boolean, rpc, Iterable
from pymongo import MongoClient
from services.database import Database
from pymongo.errors import PyMongoError
from datetime import datetime, timedelta
import jwt 

salt = "salt" 
from models.auth_models import LoginRequest, LoginResponse, RegisterRequest, RegisterResponse, RegisterDOtpRequest, RegisterDOtpResponse
class ClientService(ServiceBase):
    @rpc(LoginRequest, _returns=LoginResponse)
    def Login(ctx,req):
        doc = Database.GetInstance().clients.find_one( {"id_customer": req.username})

        if (doc is None):
            return LoginResponse(status=False, message="Sai ten dang nhap ")

        db_password = doc["password"] 
        if bcrypt.checkpw(req.password.encode("utf-8"),db_password.encode("utf-8")):
            # Create jwt 
            payload = {
                "id_customer" : doc["id_customer"],
                 "exp" : datetime.now() + timedelta(days=5)
            } 
            token = jwt.encode(payload, salt, algorithm="HS256")

            res = Database.GetInstance().clients.find_one_and_update({ "id_customer" : req.username }, {"$set" : {"session_key" : token}})
            if ( "dotp" in res ): 
                dotp = True
            else :
                dotp = False

            return LoginResponse(
                status=True, id_customer=doc["id_customer"], fullname=doc["fullname"], phone=doc["phone"], session_key=token, dotp=dotp
            ) 
        return LoginResponse ( status=False, message = "Mat khau khong chinh xac")

    @rpc(RegisterRequest, _returns=RegisterResponse)
    def Register(ctx,req):
        plain_password = req.password.encode("utf-8") 
        hash_password = bcrypt.hashpw(plain_password, bcrypt.gensalt())

        doc =  Database.GetInstance().clients.find_one({"id_customer " : req.id_customer})
        if (doc is dict):
            return RegisterResponse(status=False, message="Tai khoan da duoc dang ki")
        else:
            data = {
                "id_customer" : req.id_customer, 
                "fullname" : req.fullname,
                "email" : req.email, 
                "phone" : req.phone, 
                "password" : hash_password.decode()
            }
            result = Database.GetInstance().clients.insert_one(data)
            return RegisterResponse(status=True, message="Dang ki thanh cong") 


    @rpc(RegisterDOtpRequest,  _returns=RegisterDOtpResponse)
    def RegisterDOtp(ctx, req): 
        doc = Database.GetInstance().clients.find_one({"id_customer" : req.id_customer}) 
        if doc["session_key"] == req.session_key :  
            plain_dotp = req.dotp.encode("utf-8")
            hash_dotp = bcrypt.hashpw(plain_dotp, bcrypt.gensalt())
            Database.GetInstance().clients.update_one( { "id_customer" : req.id_customer} , { "$set" : {"dotp" : hash_dotp.decode()}})
            return RegisterDOtpResponse(status=True, message="Dang ki dotp thanh cong")
        return RegisterDOtpResponse(status=False, message = "Xac thuc khong thanh cong")
    
    
    # def ForgetPassword():
    #     return


