import json

from flask import Flask, render_template
from flask import request
from flask_socketio import SocketIO, emit, join_room

app = Flask(__name__)
app.config['SECRET_KEY'] = '@d:bFV9N7IIbbK<9u<3,I0x80we+k$!00<mEm9FD-;M(Vhtx1<3s73.VD74yg'
socketio = SocketIO(app,message_queue='redis://172.17.0.2')


@app.route("/")
def hello():
    return render_template("index.html")

@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)

@socketio.on('json')
def handle_json(json):
    print('received json: ' + str(json))


@socketio.on('connected', namespace='/test')
def handle_connected(json):
    re = request
    print re.sid
    print json


@socketio.on('me', namespace='/test')
def me():
    re = request
    print re.sid
    emit('you',{"message":re.sid})


@socketio.on('my_ping', namespace='/test')
def ping_pong():
    emit('my_pong')

@socketio.on('message_user',namespace='/test')
def message_user(arg):
    print arg
    # join_room(arg['user'])
    # room is also user
    emit('response', arg, namespace='/test',room=arg['user']);


@socketio.on('response')
def handle_response(json):
    print('received response: ' + str(json))

# This is using alternative without decorator
def handle_my_custom_event(arg):
    print('received: ' + str(arg))
    emit('response', arg, namespace='/test');

socketio.on_event('event', handle_my_custom_event, namespace='/test')


def ack():
    print 'message was received!'

@socketio.on('my event',namespace='/test')
def handle_my_custom_event(json):
    emit('my response', json, callback=ack)



if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0')