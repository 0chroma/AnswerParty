import random
from pymongo import ASCENDING
from pymongo import DESCENDING
from pyramid.exceptions import ExceptionResponse
from pyramid.response import Response

questions = ['How do I cut bread?',
             'What age should I teach my kid to shoot a gun?',
             'How many stars are there?']
MAX_IN_ROOM = 8
def home(request):
    return {}

def make_room(request):
    question = random.choice(questions)
    db = request.db
    rooms = db.rooms
    counts = db.counts
    
    counts.update({'_id':'room_id'},{'$inc':{'count':1}},upsert=True,safe=True)
    room_id = counts.find_one({'_id':'room_id'})['count']    
    rooms.insert({'_id':room_id,
                  'question':question,
                  'inRoom':[],
                  'usrCount':0,
                  'allUsrs':[],
                  'answer':"",
                  'currUsr':"",
                  'lastUsr':"",
                  'active':True
    });
    rooms.ensure_index([('active',ASCENDING),('usrCount',DESCENDING)])
    return {'question':question,'room_id':room_id}
    
def join_room(request):
    params = request.params
    
    if not 'name' in params:
        print "No Name"
        resp = Response("Must specify name",status='500')
        return resp;
        
    name = params['name']
    
    db = request.db
    rooms = db.rooms
    
    room = None
    if 'room' in params:
        room = rooms.find_one({'_id':params['room']})
    if room == None:
        roomlist = rooms.find({'active':True,'usrCount':{'$lt':MAX_IN_ROOM}}).sort('usrCount').limit(1)
    if roomlist.count() < 1:
        room_id = make_room(request)['room_id']
        room = rooms.find_one({'_id':room_id})
    else:
        room = roomlist[0]
    #TODO: Make sure name is unique
    rooms.update({'_id':room['_id']},{'$inc':{'usrCount':1},'$push':{'inRoom':name,'allUsrs':name}})
    return {'question':room['question'],'name':params['name']}
