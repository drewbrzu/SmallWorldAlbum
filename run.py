from app_package import create_app  # This goes to the /app/ directory and imports the 'app' variable from the '__init__.py' file.

app = create_app() # by default it uses our config class to set the config info for this app

if __name__ == "__main__":
    app.run(debug=True)
