
import bcrypt
from spyne import ServiceBase, Unicode, Boolean, rpc, Iterable
from pymongo import MongoClient
from database import Database
from pymongo.errors import PyMongoError

class ClientService(ServiceBase):
    @rpc(Unicode, Unicode, _return=Boolean)
    def Login(username, password):
        # trả về khóa xác thực phiên
        doc = Database.GetInstance().client.find_one( {"username": username})
        db_password = doc["password"] 
        if bcrypt.checkpwd(db_password, password):
            return True
        return False

    @rpc(Unicode, Unicode, Unicode, Unicode, Unicode, _return=Boolean)
    def Register(id_customer, phone, fullname, email, password):
        plain_password = password.encode("utf-8") 
        hash_password = bcrypt.hashpw(plain_password, bcrypt.gensalt())
        if ( Database.GetInstance().client.find_one(id) == 0): 
            return False
        data = {
            "id_customer" : id_customer, 
            "fullname" : fullname,
            "email" : email, 
            "password" : hash_password.decode()
        }
        try :
            result = Database.GetInstance().client.insert_one(data)
        except PyMongoError as e:
            print("Error : " , e)
            return False
        return True

    @rpc(Unicode,Unicode,  _return=Boolean)
    def RegisterDOtp(id, dotp): 
        Database.GetInstance().client.insert_one( { "id" : id} , { "$set" : {"dotp" : dotp}})
        return True
    
    def ForgetPassword():
        return


