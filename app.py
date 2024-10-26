import eventlet
eventlet.monkey_patch()

import os
from time import localtime, strftime
from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from wtform_fields import *
# from extensions import db  # Import db from extensions
from models import db, User


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')

db.init_app(app) # initialize db

# Initialize Flask-SocketIO
socketio = SocketIO(app)
ROOMS = ["lounge", "news", "games", "coding"]

# with app.app_context():
#     db.create_all()  # Create the database and the tables

# Configure flask login
login = LoginManager(app) # type: ignore
login.init_app(app) # type: ignore


@login.user_loader
def load_user(id):
   # 不需要： User.query.filter_by(id=id).first(), instead ->
    return User.query.get(int(id))



@app.route('/', methods=['GET', 'POST'])
def index():
    
    reg_form = RegistrationForm()

    # Updated database if validation success
    if reg_form.validate_on_submit():
        # return "Great success!"
        username = reg_form.username.data
        password = reg_form.password.data

        # Hash password
        # self-custom: using(rounds=1000, salt_size=8)
        hashed_pswd = pbkdf2_sha256.hash(password)
        
        
        # Check username exists in the db, move to the wtform
        # user_object = User.query.filter_by(username=username).first()
        # if user_object:
        #     return "Someone else has taken this username!"
        
        # Add user into DB
        user = User(username=username, password=hashed_pswd) # type: ignore
        db.session.add(user)
        db.session.commit()

        flash('Registered successfully, Please login.', 'success')

        return redirect(url_for('login'))

    return render_template('index.html', form=reg_form)




@app.route('/login', methods=['GET', 'POST'])
def login():

    login_form = LoginForm()

    # Allow login if validation success
    if login_form.validate_on_submit():
        user_object = User.query.filter_by(username=login_form.username.data).first()
        login_user(user_object)
        return redirect(url_for('chat'))

    return render_template("login.html", form=login_form)





@app.route('/chat', methods=['GET', 'POST'])
# @login_required
def chat():

    # if not current_user.is_authenticated:
    #     flash('Please login.', 'danger')
    #     return redirect(url_for('login'))

    # return 'Chat with me'
    return render_template('chat.html', username=current_user.username, rooms=ROOMS)



@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    flash('You have logged out successfully!', 'success')
    # return "Logged out using flask-logout!"
    return redirect(url_for('login'))



@socketio.on('message')
def message(data):

    print(f'\n\n{data}\n\n')  # print to the console terminal
    #send(data)      # broadcastthe pre-defined bucket called 'message' to all the clients connected at the clients' side
    # emit('some-event', 'this is a custom event message')  # send to the customed client event bucket from server
    send({'msg': data['msg'], 'username' : data['username'], 'time_stamp' : strftime('%b-%d %I:%M%p', localtime())}, room=data['room']) # type: ignore




@socketio.on('join')
def join(data):

    join_room(data['room'])
    send({'msg': data['username'] + " has jointed the " + data['room'] + " room."}, room=data['room']) # type: ignore



@socketio.on('leave')
def leave(data):

    leave_room(data['room'])
    send({'msg': data['username'] + " has left the " + data['room'] + " room."}, room=data['room']) # type: ignore





with app.app_context():
    socketio.run(app)

# if __name__ == "__main__":

#     app.run(debug=True)
#     socketio.run(app, debug=True)
    socketio.run(app)
    # socketio.run(app, host="127.0.0.1", port=80, debug=True)
# socketio.run(app)



# if __name__ == "__main__" and os.getenv("FLASK_ENV") != "production":
#     socketio.run(app, debug=True)








# ~~ python Shell

# >>> from app import app, db
# >>> app.app_context().push()
# >>> from models import User
# >>> db.create_all()
# >>> User.query.all()
# []
