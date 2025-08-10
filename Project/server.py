
from app import wsgiApp 
from wsgiref.simple_server import make_server

server = make_server('localhost', 8000, wsgiApp); 
server.serve_forever() 