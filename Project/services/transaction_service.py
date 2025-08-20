
from spyne import Boolean, ServiceBase, Int, Unicode, rpc
from services.database import Database
import bcrypt
from datetime import datetime
from models.transaction_models import BankTransferRequest, BankTransferResponse
class TransactionService(ServiceBase):

    @rpc(BankTransferRequest , _returns= BankTransferResponse)
    def BankTransfer(ctx,req): 
        doc = Database.GetInstance().account.find_one({"number_account" : req.number_account_send})
        id_customer = doc["id_customer"]
        doc = Database.GetInstance().clients.find_one({"id_customer" : id_customer})
        db_otp = doc["dotp"] 
        db_session_key = doc["session_key"]
        if (db_session_key == req.session_key and bcrypt.checkpw( req.d_otp.encode("utf-8"),db_otp.encode("utf-8"))):
            # mặc định bank_name chính là bank này namlt_banking
            # API mới chỉ hoàn thành ở mức nội bộ

            this_dict = {
                "send" : {
                    "number_account" : req.number_account_send, 
                    "bank_name" : "namlt_banking" 
                }, 
                "receiver" : {
                    "number_account" : req.number_account_receive, 
                    "bank_name" : "namlt_banking" 
                }, 
                "value" : req.value,
                "datetime": datetime.now() 
            }
            Database.GetInstance().account.update_one({"number_account" : req.number_account_send}, {"$inc" : {"balance_account" : - req.value}})
            Database.GetInstance().account.update_one({"number_account" : req.number_account_receive}, {"$inc" : {"balance_account" : req.value}})
            Database.GetInstance().transaction.insert_one(this_dict)
            return BankTransferResponse(status=True, number_account_send=req.number_account_send, number_account_receive=req.number_account_receive, value= req.value, datetime=this_dict["datetime"]);

        
        return BankTransferResponse(status=False, message="Chuyen khoan that bai") 