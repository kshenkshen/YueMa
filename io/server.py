import eventlet
eventlet.monkey_patch();
import random
import time
from threading import Timer
import socketio
from flask import Flask

PORT_SOCKETIO = 12345;

def randomSeconds():
    random.seed();
    return random.randint(5, 15);

sio = socketio.Server()
app = Flask(__name__)

Users = {};

PairingUser = [];

UserPairs = {};

def Exchange(sid, pairSid, remainingTime):
    
    if(sid in UserPairs and pairSid in UserPairs and remainingTime >= 0):
        print("Exchange.");
        sio.emit('Acquire', room=sid, namespace='/YueMa');
        sio.emit('Release', room=pairSid, namespace='/YueMa');
        seconds = randomSeconds();
        print("Next exchange at %d." % (seconds));
        Timer(seconds, Exchange, (pairSid, sid, remainingTime - seconds * 1000)).start();
    else:
        print("Not exchange.");


@app.route('/')
def index():
    return open("./static/index.html").read();

@sio.on('connect', namespace='/YueMa')
def connect(sid, environ):
    print("INFO_USER_CONNECTED: %s" % (sid));
    Users[sid] = {
        'username': ''
    };

@sio.on('disconnect', namespace='/YueMa')
def disconnect(sid):
    print("INFO_USER_DISCONNECTED: %s" % (sid));
    del Users[sid];

@sio.on('Ready', namespace='/YueMa')
def start(sid, data):
    print("INFO_READY");

    Users[sid]['username'] = data['username'];

    print(Users);

    if(len(PairingUser) == 0):
        PairingUser.append(sid);

    elif(len(PairingUser) == 1):
        pairSid = PairingUser.pop();

        UserPairs[pairSid] = sid;
        UserPairs[sid] = pairSid;

        data = {
            'task': '<div><h2>Helloworld</h2><div>Complete a simple Helloworld program with your partner.</div></div>',
            'deadline': 30000,
        };

        sio.emit('Start', data, room=sid, namespace='/YueMa');
        sio.emit('Start', data, room=pairSid, namespace='/YueMa');

        Exchange(sid, pairSid, data['deadline']);

@sio.on('Submit', namespace='/YueMa')
def start(sid, data):
    print("INFO_SUBMIT");

    print(UserPairs);

    pairSid = UserPairs[UserPairs[sid]];

    del UserPairs[UserPairs[sid]];
    del UserPairs[sid];

    print(UserPairs);

    data = {
        'score': 100,
    };

    sio.emit('Result', data, room=sid, namespace='/YueMa');
    sio.emit('Result', data, room=pairSid, namespace='/YueMa');

if __name__ == '__main__':
    app = socketio.Middleware(sio, app);

    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', PORT_SOCKETIO)), app);