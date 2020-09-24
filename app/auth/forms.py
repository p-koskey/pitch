from flask_wtf import FlaskForm
from flask import flash
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import Required,Email,EqualTo
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms import ValidationError
from ..models import User


class RegistrationForm(FlaskForm):
    email = StringField('Your Email Address:',validators=[Required(),Email()])
    username = StringField('Enter your username:',validators = [Required()])
    password = PasswordField('Password:',validators = [Required(), EqualTo('password_confirm',message = 'Passwords must match')])
    password_confirm = PasswordField('Confirm Password:',validators = [Required()])
    submit = SubmitField('Sign Up')

    def validate_email(self,data_field):
            if User.query.filter_by(email =data_field.data).first():
                flash ('There is an account with that email', 'danger')

    def validate_username(self,data_field):
        if User.query.filter_by(username = data_field.data).first():
            flash('That username is taken', 'danger')

    def validate_password(self,pass1=password,pass2=password_confirm):
        if pass1 is not pass2:
            flash('Passwords must match','danger')

class LoginForm(FlaskForm):
    email = StringField('Your Email Address:',validators=[Required(),Email()])
    password = PasswordField('Password:',validators =[Required()])
    remember = BooleanField('Remember me:')
    submit = SubmitField('Sign In')