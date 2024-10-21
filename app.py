from flask import Flask, render_template
from wtform_fields import *
# from flask_sqlalchemy import SQLAlchemy
from extensions import db  # Import db from extensions
from models import User


app = Flask(__name__)
app.secret_key = 'secret'

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'

db.init_app(app) # initialize db

# with app.app_context():
#     db.create_all()  # Create the database and the tables

@app.route('/', methods=['GET', 'POST'])
def index():
    
    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
        # return "Great success!"
        username = reg_form.username.data
        password = reg_form.password.data

        # Check username exists in the db
        user_object = User.query.filter_by(username=username).first()
        if user_object:
            return "Someone else has taken this username!"
        
        # Add user into DB
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return "A user is inserted into DB!"

    return render_template('index.html', form=reg_form)


if __name__ == "__main__":

    app.run(debug=True)


# ~~ python Shell

# >>> from app import app, db
# >>> app.app_context().push()
# >>> from models import User
# >>> db.create_all()
# >>> User.query.all()
# []