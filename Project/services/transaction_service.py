
from spyne import Boolean, ServiceBase, Int, Unicode, rpc
from database import Database
import bcrypt
from datetime import datetime
class TransactionBase(ServiceBase):

    @rpc(Unicode, Unicode, Unicode, Int,  _return=True)
    def ChuyenKhoan(send_account_number, receiver_account_number, receiver_bank_name,value, dotp): 
        doc = Database.GetInstance().account.find_one({ })
        db_otp = doc["dotp"] 
        if (bcrypt.checkpw(dotp,db_otp)):
            this_dict = {
                "send" : {
                    "account_number" : send_account_number, 
                    "bank_name" : "nltbank" 
                }, 
                "receiver" : {
                    "account_number" : receiver_account_number, 
                    "bank_name" : receiver_bank_name 
                }, 
                "value" : value,
                "datetime": datetime.now() 
            }
            # Tru tai khoan chuyen khoan, cong tai khoan chuyen khoan
            return True
        
        return False 