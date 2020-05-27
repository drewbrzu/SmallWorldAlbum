""" REFERENCES
- Working with WT-Forms: https://flask.palletsprojects.com/en/1.1.x/patterns/wtforms/
"""

from flask import render_template, url_for, flash, redirect, request
from app_package import app, db, bcrypt
from app_package.forms import RegistrationForm, LoginForm, UpdateAccountForm
from app_package.models import User
from flask_login import login_user, current_user, logout_user, login_required
# import secrets
# import os
# from PIL import Image

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

# def save_picture(form_picture):
#     random_hex = secrets.token_hex(8) # Create a random 8 digit hexadecial to use as the file name
#     f_name, f_ext = os.path.splitext(form_picture.filename) # This os function returns 2 parameters: the filename without extension, and the filename extension
#     picture_fn = random_hex + f_ext
#     picture_path = os.path.join(app.root_path, 'static/images', picture_fn) # This creates the full file path to the image.

#     output_size = (125, 125) # x/y size of picture
#     i = Image.open(form_picture) # use the PIL library to open image object
#     i.thumbnail(output_size) # resize the image.
#     i.save(picture_path) # This saves the file to the newly created path.
#     return picture_fn # return the new hexadecial filename we created.


@app.route("/user_preferences", methods=["GET", "POST"])
@login_required
def user_preferences():
    form = UpdateAccountForm()
    if request.method == 'POST' and form.validate():
        # if form.picture.data:
        #     picture_name = save_picture(form.picture.data)
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.firstname = form.first_name.data
        current_user.lastname = form.last_name.data
        db.session.commit()
        flash('Your account information has been updated!', 'success')
        return redirect(url_for('user_preferences'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.first_name.data = current_user.firstname
        form.last_name.data = current_user.lastname
    return render_template('user_preferences.html', form=form)


"""
@app.route(
    "/<pathname>"
)  # This function will pass whatever text is entered after '/' to this function as a parameter, in this case 'pathname'
def generic(pathname):
    return f"Hello, {pathname}"
 """

