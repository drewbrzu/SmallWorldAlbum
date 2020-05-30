from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from tempfile import mkdtemp
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from app_package.config import Config


# Extensions must be created outside of the app instance, but they will be initialized within the create_app method
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login' # If someone tries to access a route that requires to be logged in, they will instead be redirected to the 'login' route.
login_manager.login_message_category = 'info' # This is what css class should be used to format the message.



def create_app(config_class=Config):
    # Configure application
    app = Flask(__name__)
    app.config.from_object(Config)

    # Some imports need to be down here so that we don't have circular references
    from app_package.users.routes import users
    from app_package.main.routes import main
    app.register_blueprint(users)
    app.register_blueprint(main)

    # Intialize the extensions with this particular instance of the app
    # https://flask-sqlalchemy.palletsprojects.com/en/2.x/contexts/
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    return app

''' Erases database and recreates with default values. '''
def setup_db(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from app_package.models import State

    with app.app_context():
        db.drop_all()
        db.create_all()
        db.session.commit()
        
        state = State(name="Alaska", abreviation="AK")
        db.session.add(state)
        state = State(name="Hawaii", abreviation="HI")
        db.session.add(state)
        state = State(name="Alabama", abreviation="AL")
        db.session.add(state)
        state = State(name="Arkansas", abreviation="AR")
        db.session.add(state)
        state = State(name="Arizona", abreviation="AZ")
        db.session.add(state)
        state = State(name="California", abreviation="CA")
        db.session.add(state)
        state = State(name="Colorado", abreviation="CO")
        db.session.add(state)
        state = State(name="Connecticut", abreviation="CT")
        db.session.add(state)
        state = State(name="Delaware", abreviation="DE")
        db.session.add(state)
        state = State(name="Florida", abreviation="FL")
        db.session.add(state)
        state = State(name="Georgia", abreviation="GA")
        db.session.add(state)
        state = State(name="Iowa", abreviation="IA")
        db.session.add(state)
        state = State(name="Idaho", abreviation="ID")
        db.session.add(state)
        state = State(name="Illinois", abreviation="IL")
        db.session.add(state)
        state = State(name="Indiana", abreviation="IN")
        db.session.add(state)
        state = State(name="Kansas", abreviation="KS")
        db.session.add(state)
        state = State(name="Kentucky", abreviation="KY")
        db.session.add(state)
        state = State(name="Louisiana", abreviation="LA")
        db.session.add(state)
        state = State(name="Massachusetts", abreviation="MA")
        db.session.add(state)
        state = State(name="Maryland", abreviation="MD")
        db.session.add(state)
        state = State(name="Maine", abreviation="ME")
        db.session.add(state)
        state = State(name="Michigan", abreviation="MI")
        db.session.add(state)
        state = State(name="Minnesota", abreviation="MN")
        db.session.add(state)
        state = State(name="Missouri", abreviation="MO")
        db.session.add(state)
        state = State(name="Mississippi", abreviation="MS")
        db.session.add(state)
        state = State(name="Montana", abreviation="MT")
        db.session.add(state)
        state = State(name="North Carolina", abreviation="NC")
        db.session.add(state)
        state = State(name="North Dakota", abreviation="ND")
        db.session.add(state)
        state = State(name="Nebraska", abreviation="NE")
        db.session.add(state)
        state = State(name="New Hampshire", abreviation="NH")
        db.session.add(state)
        state = State(name="New Jersey", abreviation="NJ")
        db.session.add(state)
        state = State(name="New Mexico", abreviation="NM")
        db.session.add(state)
        state = State(name="Nevada", abreviation="NV")
        db.session.add(state)
        state = State(name="New York", abreviation="NY")
        db.session.add(state)
        state = State(name="Ohio", abreviation="OH")
        db.session.add(state)
        state = State(name="Oklahoma", abreviation="OK")
        db.session.add(state)
        state = State(name="Oregon", abreviation="OR")
        db.session.add(state)
        state = State(name="Pennsylvania", abreviation="PA")
        db.session.add(state)
        state = State(name="Rhode Island", abreviation="RI")
        db.session.add(state)
        state = State(name="South Carolina", abreviation="SC")
        db.session.add(state)
        state = State(name="South Dakota", abreviation="SD")
        db.session.add(state)
        state = State(name="Tennessee", abreviation="TN")
        db.session.add(state)
        state = State(name="Texas", abreviation="TX")
        db.session.add(state)
        state = State(name="Utah", abreviation="UT")
        db.session.add(state)
        state = State(name="Virginia", abreviation="VA")
        db.session.add(state)
        state = State(name="Vermont", abreviation="VT")
        db.session.add(state)
        state = State(name="Washington", abreviation="WA")
        db.session.add(state)
        state = State(name="Wisconsin", abreviation="WI")
        db.session.add(state)
        state = State(name="West Virginia", abreviation="WV")
        db.session.add(state)
        state = State(name="Wyoming", abreviation="WY")
        db.session.add(state)

        db.session.commit()