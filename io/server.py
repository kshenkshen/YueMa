import socketio
import eventlet
from flask import Flask

PORT_SOCKETIO = 12345;

Users = {};

sio = socketio.Server()
app = Flask(__name__)

@app.route('/')
def index():
    return open("./static/index.html").read();

@sio.on('connect', namespace='/YueMa')
def connect(sid, environ):
    print("INFO_USER_CONNECTED: %s" % (sid));

@sio.on('disconnect', namespace='/YueMa')
def disconnect(sid):
    print("INFO_USER_DISCONNECTED: %s" % (sid));

@sio.on('get_profile', namespace='/YueMa')
def get_profile(sid, data):
    print("INFO_GET_PROFILE");
    sio.emit("profile", [{ "id": 1, "nickname": "evshiron", "attributes": {
        "responsibility": 5.0, # For blames and fixes.
        "efficiency": 5.0, # For code / time.
        "reputation": 5.0, # From other users.
    } }], room = sid, namespace = "/YueMa");

@sio.on('get_rooms', namespace='/YueMa')
def get_profile(sid, data):
    print("INFO_GET_ROOMS");
    sio.emit("rooms", [{ "id": 1 }]);

@sio.on('get_users', namespace='/YueMa')
def get_profile(sid, data):
    print("INFO_GET_USERS");
    sio.emit("users", [{ "id": 1, "nickname": "evshiron" }]);

if __name__ == '__main__':
    app = socketio.Middleware(sio, app);

    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', PORT_SOCKETIO)), app);