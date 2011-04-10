import random
from pymongo import ASCENDING
from pymongo import DESCENDING
from pyramid.exceptions import NotFound
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
    if len(room['inRoom']) == 0:
        rooms.update({'_id':room['_id']},{'$inc':{'usrCount':1},'$push':{'inRoom':name,'allUsrs':name},'$set':{'currUsr':name}})
    else:
        rooms.update({'_id':room['_id']},{'$inc':{'usrCount':1},'$push':{'inRoom':name,'allUsrs':name}})
    
    session = request.session
    session['name'] = name
    session['room_id'] = room['_id']
    session.save()
    
    return {'question':room['question'],'name':params['name']}
    
def update(request):
    session = request.session
    db = request.db
    rooms = db.rooms
    
    if not 'room_id' in session:
        return NotFound()
    
    room = rooms.find_one({'_id':session['room_id']})
    currUser = room['currUsr']
    if currUser == '':
        currUser = room['inRoom'][0]
    lastUser = room['lastUsr']
    userList = room['inRoom']
    sentence = room['answer']
    isMyTurn = len(userList)<2 or (currUser == session['name'])
    
    return ({'isMyTurn':isMyTurn,
             'userList':userList,
             'sentence':sentence,
             'currUser':currUser,
             'lastUser':lastUser})
def submit_word(request):
    session = request.session
    params = request.params
    db = request.db
    rooms = db.rooms
    
    if not 'room_id' in session or not 'word' in params:
        return NotFound()
    room = rooms.find_one({'_id':session['room_id']})
    currUser = room['currUsr']
    if currUser == '':
        currUser = room['inRoom'][0]
    sentence = room['answer']
    sentence += params[word]+" "
    if len(room['inRoom']) < 2:
        return NotFound()
    
    nextUser = room['inRoom'][1]
    room.update({'_id':room['_id']},{'$pop':{'inRoom':-1},'$push':{'inRoom':currUser},'$set':{'answer':sentence,'lastUser':currUser,'currUser':nextUser}})
    return {}

def leave(request):
    session = request.session
    params = request.params
    db = request.db
    rooms = db.rooms
    
    if not 'room_id' in session:
        return NotFound()
    room = rooms.find_one({'_id':session['room_id']})
    
    leaveUser = session['name']
    room_id = session['room_id']
    del session['name']
    del session['room_id']
    
    room.update({'_id':room_id},{'$pull':{'inRoom':leaveUser},'$inc':{'usrCount':-1}})