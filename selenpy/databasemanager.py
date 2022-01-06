#%%
import pymongo
from config.settings import DATABASE
from config.variables import dbMessage

class DBMongo(object):

    def __init__(self, 
        database=DATABASE['db'],
        host=f"{DATABASE['host']}:{DATABASE['port']}",
        username=DATABASE['username'],
        password=DATABASE['password']
    ):

        self.host = host

        if username and password:
            self.client = pymongo.MongoClient(f'mongodb://{username}:{password}@{host}/')
        else:
            self.client = pymongo.MongoClient(f'mongodb://{self.host}/')

        self.db = self.client[database]

        self.status = self.client.server_info()
        try:
            print(dbMessage.okWithAuth % (
                host, username, password[-3:], 
                self.status['buildEnvironment']['target_os'],
                self.status['version']
            ))
        except TypeError:
            print(dbMessage.ok % (
                host, 
                self.status['buildEnvironment']['target_os'],
                self.status['version']
            ))

    def insertMany(self, col:str, items:list):
        self.db[col].insert_many(items, ordered=False)

    def insert(self, col:str, item:dict):
        self.db[col].insert_one(item)

    #check if an id exists in a collection
    def exists(self, col:str, id:str) -> bool:
        return self.db[col].count_documents( {'_id':id}, limit = 1 )

    #check if an collection exists in the database
    def colExists(self, col:str) -> bool:
        return col in self.db.list_collection_names()

    #count the number of documents in a collection
    def count(self, col:str) -> int:
        return self.db[col].count()

    #delete a record
    def delete(self, col:str, id:str):
        self.db[col].delete_one({'_id':id})
    
    #query records 
    def get(self, col:str, filter={}, column={}) -> list :
        return list(self.db[col].find(filter, column) )

    #update a record
    def update(self, col:str, id:str, new_value):
        self.db[col].update_one(
            { "_id":id },
            { "$set": new_value }
        )

    #update many records
    def updateMany(self, col:str, new_value, filter={}):
        self.db[col].update_many(filter, new_value)