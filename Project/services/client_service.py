
import bcrypt
from spyne import ServiceBase, Unicode, Boolean, rpc, Iterable
from pymongo import MongoClient
from database import Database
from pymongo.errors import PyMongoError
from datetime import datetime
import jwt 

salt = "salt" 
from models.auth_models import LoginRequest, LoginResponse, RegisterRequest, RegisterResponse, RegisterDOtpRequest, RegisterDOtpResponse
class ClientService(ServiceBase):
    @rpc(LoginRequest, _return=LoginResponse)
    def Login(req):
        try:
            doc = Database.GetInstance().client.find_one( {"username": req.username})
        except PyMongoError as e : 
            return LoginResponse(status=False, message = "Username khong ton tai")

        db_password = doc["password"] 
        if bcrypt.checkpwd(db_password, req.password):
            # Create jwt 
            payload = {
                "id_customer" : doc["id_customer"],
                 "time" : datetime.now() + datetime.timedelta(days= 5) 
            } 
            token = jwt.encode(payload, salt, algorithm="HS256")

            # save token in database 
            try:
                res = Database.GetInstance().session.find_one({"id_customer" : doc["id_customer"]})

                Database.GetInstance().session.update_one({ "id_customer" : doc["id_customer"] }, {"$set" : {"session_key" : token}})
            except PyMongoError as e: 
                data = {
                    "id_customer" : doc["id_customer"], 
                    "session_key" : token
                }
                Database.GetInstance().session.insert_one(data)

            return LoginResponse(
                status=True, message="", id_customer=doc["id_customer"], fullname=doc["fullname"], phone=doc["phone"], session_key=token,
            ) 
        return LoginResponse ( status=True, message = "Mat khau khong chinh xac")

    @rpc(RegisterRequest, _return=RegisterResponse)
    def Register(req):
        plain_password = req.password.encode("utf-8") 
        hash_password = bcrypt.hashpw(plain_password, bcrypt.gensalt())
        try:
            doc =  Database.GetInstance().client.find_one({"id_customer " : req.id_customer})
            return RegisterResponse(status=False, message="Tai khoan da duoc dang ki")
        except PyMongoError as e :
            data = {
                "id_customer" : req.id_customer, 
                "fullname" : req.fullname,
                "email" : req.email, 
                "password" : hash_password.decode()
            }
            try :
                result = Database.GetInstance().client.insert_one(data)
            except PyMongoError as e:
                print("Error : " , e)
            return RegisterResponse(status=True, message="Dang ki thanh cong") 


    @rpc(RegisterDOtpRequest,  _return=RegisterDOtpResponse)
    def RegisterDOtp(req): 
        try:
            doc = Database.GetInstance().session.find_one({"id_customer" : req.id_customer}) 
            if doc["session_key"] == req.session_key :  
                Database.GetInstance().client.insert_one( { "id" : id} , { "$set" : {"dotp" : req.dotp}})
                return RegisterDOtpResponse(status=True, message="Dang ki dotp thanh cong")
            return RegisterDOtpResponse(status=False, message = "Xac thuc khong thanh cong")
        except PyMongoError as e:
            return RegisterDOtpResponse(status=False, message = "None")
    
    
    def ForgetPassword():
        return


