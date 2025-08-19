
from spyne import Unicode, Boolean, ServiceBase, rpc, Iterable, Int
from services.database import Database
from datetime import datetime
from models.account_model import CreateAccountRequest, CreateAccountResponse, ChangeStatusAccountRequest, ChangeStatusAccountReponse
from pymongo.errors import PyMongoError
import bcrypt
import jwt

salt = "server"
class AccountService(ServiceBase): 
    @rpc(CreateAccountRequest, _returns=CreateAccountResponse)
    def CreateAccount(ctx,req):
        doc = Database.GetInstance().clients.find_one({"id_customer" : req.id_customer})
        db_dotp = doc["dotp"]
        db_session_key = doc["session_key"]
        if ( db_dotp == req.dotp and db_session_key == req.session_key):
            try : 
                queryNumberAccount = Database.GetInstance().account.find_one({"number_account" : req.number_account})
                return CreateAccountResponse(status=False, message="So tai khoan da ton tai")
            except PyMongoError as e: 
                this_dict = {
                    "id_customer" : req.id_customer ,
                    "number_account" : req.number_account, 
                    "balance_account" : 30000,  # tự động cộng vào tài khoản 30k
                    "status" : "active"
                }
            Database.GetInstance().account.insert_one(this_dict)
            return CreateAccountResponse(status=True, number_account=req.number_account, balance_account=req.balance_account)

        return CreateAccountResponse(status=False, message="Xac thuc khong cong")


    @rpc(ChangeStatusAccountRequest ,_returns=ChangeStatusAccountReponse) 
    def ChangeStatusAccount(ctx, req): 
        doc = Database.GetInstance().clients.find_one({"id_customer" : req.id_customer}); 
        # check cả 2
        db_dotp = doc["dotp"]
        db_session_key = doc["session_key"]
        if ( db_session_key == req.session_key and bcrypt.checkpw(req.dotp,db_dotp)):
            if ( type == 0): # tạm khóa 
                Database.GetInstance.account.update_one( 
                    {"number_account": req.number_account}, 
                    { "$set" : {
                         "status" : "lock"
                    }
                    }); 
                
                return ChangeStatusAccountReponse(status=True) 
            elif type == 1: # xóa tài khoản
                Database.GetInstance.account.delete_one({"number_account" : req.number_account})
                return ChangeStatusAccountReponse(status=True, message="Xoa so tai khoan thanh cong") 

        return ChangeStatusAccountReponse(stauts=False, message="Xac thuc that bai") 
    
   

