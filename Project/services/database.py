
from pymongo import MongoClient 

class Database:
    _instance = None # biến của class 
    
    def __new__(cls):
        if cls._instance is None: 
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.client = MongoClient('mongodb://127.0.0.1:27017')
            cls._instance.db = cls._instance.client['virtual_banking']
        return cls._instance
    
    @classmethod 
    def GetInstance(cls):
        if cls._instance is None:
            cls()
        return cls._instance.db


