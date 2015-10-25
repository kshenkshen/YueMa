import eventlet
eventlet.monkey_patch();
import random
import time
from threading import Timer
import socketio
from flask import Flask

from oj import oj

PORT_SOCKETIO = 12345;

def randomSeconds(min, max):
    random.seed();
    return random.randint(min, max);

sio = socketio.Server()
app = Flask(__name__)

Users = {};

# Difficulty.
PairingUser = {
    '0': [],
    '1': [],
    '2': [],
};

UserMatches = {};

WorkingUsers = [];

def Exchange(sid, pairSid, minTime, maxTime, remainingTime):
    
    if((sid in WorkingUsers or pairSid in WorkingUsers) and remainingTime >= 0):
        print("Exchange.");
        sio.emit('Acquire', room=sid, namespace='/YueMa');
        sio.emit('Release', room=pairSid, namespace='/YueMa');
        seconds = randomSeconds(minTime, maxTime);
        print("Next exchange at %d." % (seconds));
        Timer(seconds, Exchange, (pairSid, sid, minTime, maxTime, remainingTime - seconds * 1000)).start();
    else:
        print("Not exchange.");


@app.route('/')
def index():
    return open("./static/index.html").read();

@sio.on('connect', namespace='/YueMa')
def connect(sid, environ):
    print("INFO_USER_CONNECTED: %s" % (sid));
    Users[sid] = {
        'username': '',
        'problem': {},
        'yue': False,
    };

@sio.on('disconnect', namespace='/YueMa')
def disconnect(sid):
    print("INFO_USER_DISCONNECTED: %s" % (sid));
    try:
        del Users[sid];
        PairingUser['0'].remove(sid);
        PairingUser['1'].remove(sid);
        PairingUser['2'].remove(sid);
        pairSid = UserMatches[sid];
        del UserMatches[sid];
        del UserMatches[pairSid];
        WorkingUsers.remove(sid);
        WorkingUsers.remove(pairSid);
    except Exception as err:
        pass

@sio.on('Ready', namespace='/YueMa')
def ready(sid, data):
    print("INFO_READY");

    Users[sid]['username'] = data['username'];

    print(Users);

    if(len(PairingUser[data['difficulty']]) == 0 and sid not in PairingUser[data['difficulty']]):
        PairingUser[data['difficulty']].append(sid);

    elif(len(PairingUser[data['difficulty']]) == 1 and sid not in PairingUser[data['difficulty']]):
        pairSid = PairingUser[data['difficulty']].pop();

        UserMatches[pairSid] = sid;
        UserMatches[sid] = pairSid;

        WorkingUsers.append(sid);
        WorkingUsers.append(pairSid);

        problem = oj.random_pro(data['difficulty']);

        Users[sid]['problem'] = problem;
        Users[pairSid]['problem'] = problem;

        # TODO: Load from question library.
        data = {
            'task': problem['desc'],
            'deadline': problem['total_time'] * 1000,
        };

        sio.emit('Start', data, room=sid, namespace='/YueMa');
        sio.emit('Start', data, room=pairSid, namespace='/YueMa');

        Exchange(sid, pairSid, problem['swt_time_range'][0], problem['swt_time_range'][1], data['deadline']);

@sio.on('Update', namespace='/YueMa')
def update(sid, data):

    pass
    sio.emit('Update', data, room=UserMatches[sid], namespace='/YueMa');

@sio.on('Push', namespace='/YueMa')
def push(sid, data):

    sio.emit('Push', data, room=UserMatches[sid], namespace='/YueMa');

@sio.on('Submit', namespace='/YueMa')
def submit(sid, data):
    print("INFO_SUBMIT");

    print(WorkingUsers);

    pairSid = UserMatches[sid];

    if(sid in WorkingUsers):
        WorkingUsers.remove(sid);

    if(pairSid not in WorkingUsers):

        print(WorkingUsers);

        problem = Users[sid]['problem'];

        ret1 = oj.submit({
            'pid': problem['pid'],
            'lang': 'py',
            'code': data['code'],
        });

        ret2 = oj.submit({
            'pid': problem['pid'],
            'lang': 'c',
            'code': data['code'],
        });

        def rolling():

            try:

                if(oj.status(ret1['fid'])['status_code'] == 1 and oj.status(ret1['fid'])['status_code'] == 1):

                    data = {
                        'pass': oj.status(ret1['fid'])['ac'] or oj.status(ret2['fid'])['ac'],
                    };

                    sio.emit('Result', data, room=sid, namespace='/YueMa');
                    sio.emit('Result', data, room=pairSid, namespace='/YueMa');

                else:

                    Timer(2, rolling, ()).start();

            except Exception as err:

                data = {
                    'pass': False,
                };

                sio.emit('Result', data, room=sid, namespace='/YueMa');
                sio.emit('Result', data, room=pairSid, namespace='/YueMa');


        rolling();

@sio.on('Yue', namespace='/YueMa')
def yue(sid, data):
    print("INFO_YUE");

    pairSid = UserMatches[sid];

    Users[sid]['yue'] = True;

    if(Users[pairSid]['yue']):

        sio.emit('Yue', {
            'partnerName': Users[pairSid]['username'],
        }, room=sid, namespace='/YueMa');
        sio.emit('Yue', {
            'partnerName': Users[sid]['username'],
        }, room=pairSid, namespace='/YueMa');

@sio.on('NoYue', namespace='/YueMa')
def no_yue(sid, data):
    print("INFO_NO_YUE");

    pairSid = UserMatches[sid];

    Users[sid]['yue'] = False;
    Users[pairSid]['yue'] = False;

    #sio.emit('NoYue', {}, room=sid, namespace='/YueMa');
    sio.emit('NoYue', {}, room=pairSid, namespace='/YueMa');

@sio.on('Evaluate', namespace='/YueMa')
def evaluate(sid, data):
    print("INFO_EVALUATE");

    pairSid = UserMatches[sid];

    sio.emit('Evaluate', data, room=pairSid, namespace='/YueMa');

@sio.on('Message', namespace='/YueMa')
def message(sid, data):
    print("INFO_MESSAGE");

    pairSid = UserMatches[sid];

    sio.emit('Message', data, room=pairSid, namespace='/YueMa');

if __name__ == '__main__':
    app = socketio.Middleware(sio, app);

    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', PORT_SOCKETIO)), app);