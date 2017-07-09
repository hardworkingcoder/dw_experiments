from app import app
from flask_socketio import SocketIO
from flask_failsafe import failsafe
socketio = SocketIO(app)

@failsafe
def create_app():
    return app

import eventlet
eventlet.monkey_patch()
if __name__ == '__main__':
    socketio.run(create_app(), debug=True, use_reloader=True, port=app.config['PORT'])