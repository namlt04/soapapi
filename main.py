from spyne import Application, rpc, ServiceBase, Integer, Unicode, Boolean
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

class MySoapService(ServiceBase):
    # rpc đánh dấu phương thức đó là 1 remote procedure call ( hàm gọi từ client qua soap )
    # các tham số trong @rpc(...) định nghĩa kiểu dữ liệu tham số đầu vào và kiểu dữ liệu trả về 
    # Spyne dựa vào thông tin này để : 
    # + Tạo schema xml đúng chuẩn cho soap request/response
    # + Kiểm tra và ép kiểu dữ liệu đầu vào đầu ra 
    # + tự động chuyển đổi giữa python và kiểu dữ liệu python
    @rpc(Integer, Integer, _returns=Integer) 
    def Add(ctx, a, b):
        # ctx : context, context object
        # chứa toàn bộ thông tin về context ( ngữ cảnh ) của request hiện tại mà server đang sử lý
        # giúp truy cập dữ liệu liên quan như 
        # + thông tin http request ( headers, ip client, cookies ) 
        # + thông tin soap 
        # session, metadata
        # các dữ liệu bổ sung do bạn hoặc framework thêm vào content 

        return a + b

    @rpc(Unicode, Unicode, _returns=Boolean)
    def login(ctx, username, password):
        # Ví dụ: username='user', password='pass' thì login thành công
        if username == 'user' and password == 'pass':
            return True
        return False

# Tạo application SOAP
application = Application([MySoapService],
    tns='spyne.examples.mysoap', # target namespace : tên miền mcu5 tiêu Phân biệt các phương thức, kiểu dữ liệu của dịch vụ này với các dịch vụ khác (tránh trùng tên).

# Đảm bảo khi client và server trao đổi XML, các phần tử được hiểu đúng thuộc về dịch vụ nào.
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

wsgi_app = WsgiApplication(application)

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    port = 8000
    print(f"Starting SOAP server on port {port}...")
    server = make_server('0.0.0.0', port, wsgi_app)
    server.serve_forever()
