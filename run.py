from app_package import create_app, setup_db  # This goes to the /app/ directory and imports the 'app' variable from the '__init__.py' file.

# setup_db() should only be uncommented and run the first time the application is deployed. This function will completely erase the database and setup default values.
#setup_db()

app = create_app() # by default it uses our config class to set the config info for this app




if __name__ == "__main__":
    app.run(debug=True)
