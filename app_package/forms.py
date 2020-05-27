from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app_package.models import User


class RegistrationForm(FlaskForm):
    username = StringField("Username", 
        validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email", 
        validators=[DataRequired(), Email()])
    password = PasswordField("Password", 
        validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", 
        validators=[DataRequired(), EqualTo("password")])
    first_name = StringField("First Name", 
        validators=[DataRequired()])
    last_name = StringField("Last Name", 
        validators=[DataRequired()])
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        """ This method is a custom form validation that checks if username already exist in our database. """
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already taken. Please choose a different one.')

    def validate_email(self, email):
        """ This method is a custom form validation that checks if email already exist in our database. """
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already associated with an account. Please click forgot username/password if you forgot your username.')


class LoginForm(FlaskForm):
    username = StringField("Username", 
        validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField("Password", 
        validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


class UpdateAccountForm(FlaskForm):
    username = StringField("Username", 
        validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email", 
        validators=[DataRequired(), Email()])
    first_name = StringField("First Name", 
        validators=[DataRequired()])
    last_name = StringField("Last Name", 
        validators=[DataRequired()])

    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField("Update")

    def validate_username(self, username):
        """ This method is a custom form validation that checks if username already exist in our database. """
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is already taken. Please choose a different one.')

    def validate_email(self, email):
        """ This method is a custom form validation that checks if email already exist in our database. """
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is already associated with an account. Please click forgot username/password if you forgot your username.')