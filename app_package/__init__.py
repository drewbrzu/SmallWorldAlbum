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
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    return app