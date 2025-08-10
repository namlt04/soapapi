

from spyne import ServiceBase, Unicode, Boolean, rpc, Iterable
users = dict(); 
class AuthService(ServiceBase): 
    @rpc(Unicode, Unicode, _returns= Boolean)
    def authentication(ctx, username, password): 
        if username in users : 
            if ( users[username] == password):
                return True
        return False 
    @rpc(Unicode, Unicode, _returns=Boolean)
    def create(ctx, username, password): 
        if username in users: 
           return False
        users[username] = password
        return True 
    @rpc(Unicode, Unicode, _returns= Boolean)
    def change(ctx, username, newPassword): 
        if username in users: 
            users[username] = newPassword
            return True 
        return False
    
    @rpc(_returns = Iterable(Unicode))
    def show(ctx):
        for username in users: 
            yield username
    
        
