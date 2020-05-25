""" REFERENCES
- Working with WT-Forms: https://flask.palletsprojects.com/en/1.1.x/patterns/wtforms/
"""

from flask import render_template, url_for, flash, redirect, request
from app_package import app, db, bcrypt
from app_package.forms import RegistrationForm, LoginForm
from app_package.models import User
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/register", methods=["POST", "GET"])
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password, firstname=form.first_name.data, lastname=form.last_name.data, email=form.email.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'Welcome {user.firstname}, you have been logged in!', 'success')
            # If the user tried to get to a blocked page without being logged in, there will be a 'next' parameter in the GET request.
            # We will redirect them to this page once they login. If there isn't a 'next' parameter specified, then send them to the default 'home' page.
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout", methods=["GET"])
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/user_preferences", methods=["GET"])
@login_required
def user_preferences():
    return render_template('user_preferences.html', title='User Preferences')


"""
@app.route(
    "/<pathname>"
)  # This function will pass whatever text is entered after '/' to this function as a parameter, in this case 'pathname'
def generic(pathname):
    return f"Hello, {pathname}"
 """


# @app.route("/login", methods=["GET", "POST"])
# def login():
#     """Log user in"""

#     # Forget any user_id
#     session.clear()

#     # User reached route via POST (as by submitting a form via POST)
#     if request.method == "POST":

#         # Ensure username was submitted
#         if not request.form.get("username"):
#             return redirect("/") #error("must provide username", 403)

#         # Ensure password was submitted
#         elif not request.form.get("password"):
#             return redirect("/") #error("must provide password", 403)

#         # Query database for username
#         rows = db.execute(
#             "SELECT * FROM users WHERE username = :username",
#             username=request.form.get("username"),
#         ).fetchall()
#         # with sqlite3.connect("mydatabase.db") as con:
#         #     cur = con.cursor()
#         #     cur.execute(
#         #         "SELECT * FROM users WHERE username = ?", request.form.get("username")
#         #     )
#         #     rows = cur.fetchall()
#         #     con.commit()
#         # Query database for username
#         # rows = db.execute(
#         #     "SELECT * FROM users WHERE username = :username",
#         #     username=request.form.get("username"),
#         # )

#         # Ensure username exists and password is correct
#         if len(rows) != 1 or not check_password_hash(
#             rows[0]["hash"], request.form.get("password")
#         ):
#             return redirect("/") #error("invalid username and/or password", 403)

#         # Remember which user has logged in
#         session["user_id"] = rows[0]["id"]

#         # Redirect user to home page
#         return redirect("/")

#     # User reached route via GET (as by clicking a link or via redirect)
#     # Display the page for user to enter their info to log in.
#     else:
#         return render_template("login.html")


# @app.route("/forgotpassword", methods=["GET", "POST"])
# def forgotpassword():
#     if request.method == "POST":
#         if not request.form.get("email"):
#             return redirect("/")  # error("please enter an email address")
#         return redirect("/")
#     else:
#         return render_template("user_account/forgotpassword.html")


# @app.route("/register", methods=["GET", "POST"])
# def register():
#     if request.method == "POST":
#         # Grab form data
#         username = request.form.get("username")
#         password = request.form.get("password")
#         password2 = request.form.get("password2")
#         firstname = request.form.get("firstname")
#         lastname = request.form.get("lastname")
#         email = request.form.get("email")

#         # Check form inputs
#         if (
#             not username
#             or not password
#             or not password2
#             or not firstname
#             or not lastname
#             or not email
#         ):
#             return redirect("/") #error("please enter all information.")

#         if not password == password2:
#             return redirect("/") #error("passwords must match.")

#         if not "@" in email:
#             return redirect("/") #error("please enter a valid email.")

#         queryRes = db.execute(
#             "SELECT username FROM users WHERE username = :username", username=username
#         ).fetchall()

#         # Start database
#         # with sqlite3.connect("mydatabase.db") as con:
#         #     cur = con.cursor()
#         #     cur.execute("SELECT username FROM users WHERE username = ?", (username))
#         #     queryRes = cur.fetchall()
#         #     con.commit()

#         if len(queryRes) < 1:
#             db.execute(
#                 "INSERT INTO users (username, hash, firstname, lastname, email) VALUES (:username, :hash, :fname, :lname, :email)",
#                 username=username,
#                 hash=generate_password_hash(password),
#                 fname=firstname,
#                 lname=lastname,
#                 email=email,
#             )
#             # with sqlite3.connect("mydatabase.db") as con:
#             #     cur = con.cursor()
#             #     cur.execute(
#             #         "INSERT INTO users (username, hash, firstname, lastname, email) VALUES (?, ?, ?, ?, ?)",
#             #         (
#             #             username,
#             #             generate_password_hash(password),
#             #             firstname,
#             #             lastname,
#             #             email,
#             #         ),
#             #     )
#             #     con.commit()
#             redirect("/login")
#         else:
#             error("Sorry, that username is already taken.")
#         return redirect("/")

#     else:
#         return render_template("user_account/register.html")


# @app.route("/logout")
# def logout():
#     """Log user out"""

#     # Forget any user_id
#     session.clear()

#     # Redirect user to login form
#     return redirect("/")
