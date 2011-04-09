from pyramid.decorator import reify
from pyramid.request import Request
from pymongo import Connection
import gridfs
#import redis

class RequestWithDB(Request):
    @reify
    def db(self):
        connection = Connection('localhost',27017)
        return connection['lemon']
    #@reify
    #def gridFS(self):
    #    return gridfs.GridFS(self.db, self.registry['gridFS_collection'])
    #@reify
    #def redis(self):
    #    return redis.Redis(host='localhost', port=6379, db=0)

