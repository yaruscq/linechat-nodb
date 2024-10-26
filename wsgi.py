import eventlet
eventlet.monkey_patch()

from app import socketio, app


# with app.app_context():
#     socketio.run(app)

if __name__ == "__main__":
    socketio.run(app)

