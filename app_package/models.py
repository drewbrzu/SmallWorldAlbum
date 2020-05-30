from flask import current_app
from app_package import db, login_manager  # import the db and login_manager variables from our app package file
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/#many-to-many-relationships
statesVisited = db.Table('statesvisited',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('state_id', db.Integer, db.ForeignKey('state.id'), primary_key=True)
)

class User(db.Model, UserMixin): # This class inherits from both 'db.model' and 'UserMixin'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    statesVisited = db.relationship('State', secondary=statesVisited, lazy='subquery', backref=db.backref('users', lazy=True))

    def __repr__(self): # This method already has default behavior defined for all classes. This method returns a value to represent this class
        return f"User('{self.firstname}', '{self.lastname}')"

class State(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    abreviation = db.Column(db.String(2), nullable=False, unique=True)
