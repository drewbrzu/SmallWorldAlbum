from app_package import db, login_manager  # import the db and login_manager variables from our app package file
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin): # This class inherits from both 'db.model' and 'UserMixin'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)

    def __repr__(self): # This method already has default behavior defined for all classes. This method returns a value to represent this class
        return f"User('{self.firstname}', '{self.lastname}')"


