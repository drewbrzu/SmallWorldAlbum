from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from tempfile import mkdtemp
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# Configure application
app = Flask(__name__)

# Setup app configureation
app.config["SECRET_KEY"] = "123456789"  # Protects against modifying cookies, cross-site forgery attacks
app.config["TEMPLATES_AUTO_RELOAD"] = True  # Ensure templates are auto-reloaded
app.config["SESSION_FILE_DIR"] = mkdtemp()  # Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydatabase.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login' # If someone tries to access a route that requires to be logged in, they will instead be redirected to the 'login' route.
login_manager.login_message_category = 'info'

# Some imports need to be down here so that we don't have circular references
from app_package import routes
