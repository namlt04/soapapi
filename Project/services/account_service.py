
from spyne import Unicode, Boolean, ServiceBase, rpc, Iterable, Int
from services.database import Database
from datetime import datetime
from models.account_models import CreateAccountRequest, CreateAccountResponse, ChangeStatusAccountRequest, ChangeStatusAccountReponse, ListNumberAccountRequest, ListNumberAccountResponse, NumberAccount
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
        if ( bcrypt.checkpw( req.dotp.encode("utf-8"),db_dotp.encode("utf-8")) and db_session_key == req.session_key):
                res = Database.GetInstance().account.find_one({"number_account" : req.number_account})
                if  (res is not None):
                    return CreateAccountResponse(status=False, message="So tai khoan da ton tai")
                else:
                    this_dict = {
                        "id_customer" : req.id_customer ,
                        "number_account" : req.number_account, 
                        "balance_account" : 30000,  # tự động cộng vào tài khoản 30k
                        "status" : "active"
                    }
                    Database.GetInstance().account.insert_one(this_dict)
                    return CreateAccountResponse(status=True, number_account=req.number_account, balance_account=this_dict["balance_account"])

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

    
    @rpc(ListNumberAccountRequest, _returns=ListNumberAccountResponse) 
    def ListNumberAccount(ctx, req):
        res = Database.GetInstance().clients.find_one({"id_customer" : req.username})
        db_session_key = res["session_key"]
        res = Database.GetInstance().account.find({"id_customer" : req.username})
        res = list(res)
        if ( len(res) >= 1):
            if (req.session_key == db_session_key):
                array = list()
                for doc in res:
                    array.append(NumberAccount(number_account= doc["number_account"],balance_account=doc["balance_account"] , status= doc["status"]))
                return ListNumberAccountResponse(status=True, account = array)
        else :
            return ListNumberAccountResponse(status=True, account = [])  

        return ListNumberAccountResponse(status=False, message="Xac thuc khong thanh cong")
   

