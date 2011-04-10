import random

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
    #rooms.ensure_index([{'active':1},{'usrCount':-1}])
    return {'question':question,'room_id':room_id}
    
def join_room(request):
    params = request.params
    return {'question':random.choice(questions),'name':params['name']}
    #name = params['name']
    #
    #db = request.db
    #rooms = db.rooms
    #
    #room = None
    #if 'room' in params:
    #    room = rooms.find_one({'_id':params['room']})
    #if room == None:
    #    room = rooms.find_one({'active':True,'usrCount':{'$lt':MAX_IN_ROOM}},sort={})
    #    
