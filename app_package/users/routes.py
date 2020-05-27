""" REFERENCES
- Working with WT-Forms: https://flask.palletsprojects.com/en/1.1.x/patterns/wtforms/
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from app_package import db, bcrypt
from app_package.models import User
from app_package.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm)
# from app_package.users.utils import 

users = Blueprint('users', __name__)

@users.route("/register", methods=["POST", "GET"])
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password, firstname=form.first_name.data, lastname=form.last_name.data, email=form.email.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)

@users.route("/login", methods=["POST", "GET"])
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
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@users.route("/logout", methods=["GET"])
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route("/user_preferences", methods=["GET", "POST"])
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
        return redirect(url_for('users.user_preferences'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.first_name.data = current_user.firstname
        form.last_name.data = current_user.lastname
    return render_template('user_preferences.html', form=form)