from spyne import Application
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

from services.auth_service import AuthService
application = Application([AuthService], tns= "http://thanhnam.com/admin", in_protocol=Soap11(validator='lxml'), out_protocol=Soap11())
wsgiApp = WsgiApplication(application)