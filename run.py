from app_package import (app)  # This goes to the /app/ directory and imports the 'app' variable from the '__init__.py' file.

if __name__ == "__main__":
    app.run(debug=True)