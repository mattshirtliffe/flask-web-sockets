
from flask_socketio import SocketIO


def alert():
    socketio = SocketIO(message_queue='redis://172.17.0.2')
    #  we can pass sid as room to send message to a specific user
    socketio.emit('alert', {"message":"fuckyou"}, namespace='/test');


if __name__ == '__main__':
    alert()