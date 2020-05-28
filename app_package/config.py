# dotenv allows us to load environment variables that are saved to the .env file. This is useful for loading secret information like the database connection string.
# https://pybit.es/persistent-environment-variables.html
from dotenv import load_dotenv 
import os


class Config:
    # Setup app configuration
    SECRET_KEY = os.getenv("SECRET_KEY")  # Protects against modifying cookies, cross-site forgery attacks
    TEMPLATES_AUTO_RELOAD = True  # Ensure templates are auto-reloaded

    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False