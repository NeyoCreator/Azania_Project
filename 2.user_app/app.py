
from email import message
from flask import Flask, render_template,redirect,url_for 
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,BooleanField
from wtforms.validators import InputRequired, Email, Length
import email_validator
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import json

file_path = os.path.abspath(os.getcwd())+"\database.db"
app = Flask(__name__)
app.config['SECRET_KEY']='RThsiissecrete!'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+file_path
Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'



class User(UserMixin,db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(15),unique=True)
    email = db.Column(db.String(50),unique=True)
    password=db.Column(db.String(80))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('username',validators = [InputRequired(), Length(min=4, max=15 )])
    password = PasswordField('password', validators = [InputRequired(),Length(min=8, max=80)])
    remember = BooleanField('remember')

class RegisterForm(FlaskForm):
    email = StringField('email', validators= [InputRequired(),Email(message='Invalid email'), Length(max=50)])
    username = StringField('username',validators= [InputRequired(), Length(min=4, max=15 )])
    password = PasswordField('password', validators= [InputRequired(),Length(min=8, max=80)])

class UserDetailForm(FlaskForm):
    location = StringField('location',validators = [InputRequired(), Length(min=4, max=8 )])
    destination = StringField('destination',validators = [InputRequired(), Length(min=4, max=8 )])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()  
        if user :
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))
        return '<h1>Invalid username or password</h1>'
    return render_template('login.html',form=form)

@app.route('/signup',methods=['GET','POST'])
def signup():
    form = RegisterForm()
    global username
    if form.validate_on_submit():
        username = form.username.data
        hashed_password=generate_password_hash(form.password.data, method="sha256")
        new_user = User(username=form.username.data,email=form.email.data,password = hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return '<h1>New User has been created</h1>'
    return render_template('signup.html',form=form)

@app.route('/dashboard',methods=['GET','POST'])
@login_required
def dashboard():
    form = UserDetailForm()

    with open('user_details.json') as f:
        initial_data = json.load(f)
        

    data_user = {"id":current_user.id,"username":current_user.username,"location":form.location.data, "destination":form.destination.data}
    
    initial_data.append(data_user)
    with open('user_details.json', 'w') as fp:
         json.dump(initial_data, fp)


    return render_template('dashboard.html',form =form)
    
@app.route('/logout')
@login_required
def logout():
    logout_user
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)