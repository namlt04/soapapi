
from spyne import Unicode, Boolean, ServiceBase, rpc, Iterable, Int
from database import Database
from datetime import datetime
import bcrypt

class AccountService(ServiceBase): 
    @rpc(Unicode, _return=Boolean)
    def CreateAccount(so_tai_khoan, id):
        if ((so_tai_khoan)):
            return False
        else:
            this_dict = {
                "client_id" : id,
                "number_account" : so_tai_khoan, 
                "balance_account" : 30000,  # tự động cộng vào tài khoản 30k
                "status" : "active"
            }
            Database.GetInstance().account.insert_one(this_dict)
        return True

    @rpc(Unicode, Unicode, int,_return=Boolean) 
    def ChangeStatusAccount(account_number, dotp, type): 
        # phia client tu dong kiem tra so du tai khoan
        # xóa và tạm khóa tài khoản
        doc = Database.GetInstance().client.find_one({id}); 
        if doc is None: 
            return False 
        db_dotp = doc["dotp"]

        if ( bcrypt.checkpw(dotp,db_dotp)):
            if ( type == 0): # tạm khóa 

                Database.GetInstance.account.update_one( 
                    {account_number : account_number}, 
                    { "$set" : {
                         "status" : "lock"
                    }
                    }); 
            elif type == 1: # xóa tài khoản
                Database.GetInstance.account.delete_one({account_number : account_number})

            return True
        return False
    
   

