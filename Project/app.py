from spyne import Application
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

from services.account_service import AccountService 
from services.client_service import ClientService
from services.transaction_service import TransactionService

application = Application([AccountService, ClientService, TransactionService], tns= "http://thanhnam.com/banking", in_protocol=Soap11(validator='lxml'), out_protocol=Soap11())

wsgiApp = WsgiApplication(application)