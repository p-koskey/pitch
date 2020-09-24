from . import auth
from flask import render_template,redirect,url_for, flash,request
from ..models import User
from .forms import RegistrationForm
from .. import db
from flask_login import login_user,logout_user,login_required
from ..models import User
from .forms import LoginForm,RegistrationForm
from flask_mail import Message
from .. import mail


@auth.route('/login',methods=['GET','POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        if user is not None and user.verify_password(login_form.password.data):
            login_user(user,login_form.remember.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        else:
            flash('Login Unsuccessful. please check email and password', 'danger')
        
       

    title = "Pitches login"
    return render_template('auth/login.html',login_form = login_form,title=title)

@auth.route('/register',methods = ["GET","POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email = form.email.data, username = form.username.data,password = form.password.data)
        db.session.add(user)
        db.session.commit()

        flash('Your account has been created! You are now able to login','success')
        msg = Message(subject="Pitches Account", sender="testingemailpk6@gmail.com", recipients=[user.email])
        msg.body = f"Hello "+ user.username.capitalize()+", Welcome to Pitches, We have just seen you have signed up for our application and want to welcome you to the family. Please enjoy."
        mail.send(msg)
        
        return redirect(url_for('auth.login'))
               
         
    return render_template('auth/register.html',registration_form = form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))