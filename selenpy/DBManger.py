#%%
import pymongo
from .common.settings import DATABASE
from .common.variables import dbMessage

from .common.variables import Mode
import socket
from pymongo.errors import DuplicateKeyError
import random

class MongoManger(object):

    def __init__(self, 
        database=DATABASE['db'],
        host=f"{DATABASE['host']}:{DATABASE['port']}",
        username=DATABASE['username'],
        password=DATABASE['password']
    ):

        self.host = host
        self.proxy = ProxyManager(db=self)

        if username and password:
            self.client = pymongo.MongoClient(f'mongodb://{username}:{password}@{host}/')
        else:
            self.client = pymongo.MongoClient(f'mongodb://{self.host}/')

        self.db = self.client[database]

        self.status = self.client.server_info()
        try:
            print(dbMessage.serverOkwithAuth(
                host, username, password[-3:], 
                self.status['buildEnvironment']['target_os'],
                self.status['version']
            ))
        except TypeError:
            print(dbMessage.serverOk(
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

    def dropAll(self, col:str):
        self.db[col].delete_many({})

class ProxyManager():

    def __init__(self, db):
        self.db = db
        
    def fetchProxy():
        return []

    def loadProxy(self, proxies, t):

        count = 0

        for proxy in proxies:

            try:
                host = proxy['host']
            except KeyError:
                continue
            else:
                try:
                    socket.inet_aton(host.split(":")[0])
                except OSError:
                    continue

            try:
                region = proxy['region']
            except KeyError:
                region = None

            try:
                type = proxy['type']
            except KeyError:
                if t:
                    type = t
                else:
                    type = Mode.DEFAULT

            try:
                self.db.insert("proxy",{
                    '_id':host,
                    'region':region,
                    'status':"A",
                    'type':type,
                })
                count += 1
            except DuplicateKeyError:
                self.db.update("proxy", host, {
                    'region':region,
                    'status':"A",
                    'type':type,
                })

        print(f"\r💾 {count} proxies loaded")

    def getProxy(self, type=Mode.LOCAL):

        #if no proxy
        if type==Mode.LOCAL:
            return Mode.LOCAL
        #if proxies
        else:
            proxies = list(self.db.get("proxy", filter={"status":"A", "type":f"{type}"}))

            #try to obtain one proxy
            try:
                proxy = proxies[random.randint(0, len(proxies))]["_id"]
            #if running out, return no proxy
            except IndexError:
                return Mode.LOCAL
            #mark proxy as using
            else:
                self.db.update(col="proxy", id=proxy, new_value={"status":socket.gethostname()})
                return proxy

    def resetProxies(self):
        self.db.updateMany("proxy", { "$set": {"status":"A"}})

    def releaseProxy(self, proxy):
        self.db.update(col="proxy", id=proxy, new_value={"status":"A"})

    def removeProxy(self, proxy):
        self.db.delete("proxy", proxy)

    def clearProxies(self):
        self.db.dropAll("proxy")