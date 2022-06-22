#0.IMPORT LIBRARIES
from email import message
from locale import currency
import requests
from flask import jsonify,request
from cv2 import subtract
from django.forms import IntegerField
from flask import Flask, render_template,redirect,url_for,flash ,jsonify, Response, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,BooleanField,IntegerField
from wtforms.validators import InputRequired, Email, Length
import email_validator
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import json
import qrcode
import random
import wtforms
# from camera import VideoCamera

#1.DATABASE AND FOLDER CREATION
file_path = os.path.abspath(os.getcwd())+"\databases\database.db"
app = Flask(__name__)
app.config['SECRET_KEY']='RThsiissecrete!'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+file_path
picFolder = os.path.join('static','pics')
app.config['UPLOAD_FOLDER']=picFolder

#2.LOGIN MANAGEMENT
Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


#2.2 SUBTLE
file= open('databases/user_list.json')
original_user_list = json.load(file)


#3.CLASS CREATION
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

class TokeAmount(FlaskForm):
    amount = IntegerField('ZA')
    username = wtforms.SelectField(label='username', choices=original_user_list)
    x = 7
    x = x+2
    print(x)

def kaba():
    print("Kaba")
#4.CUSTOM FUNCTIONS
#4.1 FIND CURRENT USER
def find_current_user():
    #4.1.1WRITE TO THE JSON FILE
    positional_value = 0
    with open('databases/user_details.json') as f:
        initial_data = json.load(f)
    data_user = {"id":current_user.id,"username":current_user.username,"balance":100}
    isThere=False
    

    #4.1.2.CHECK IF USER EXIST IN FILE
    for index,value in enumerate(initial_data):
        if current_user.id == value["id"]:
            isThere = True
            positional_value = index
            initial_data= initial_data[index]

    if isThere :
        data=initial_data
         #CLACULATE THE CURRENCY
        currency = data["balance"]*16   
    else:
        data=data_user
        initial_data.append(data_user)
        with open('databases/user_details.json', 'w') as fp:
            json.dump(initial_data, fp)
        #CLACULATE THE CURRENCY
        currency = data["balance"]*16

        #EDIT MASTER DATA
        with open('databases/bank.json') as f:
            current_balance_list = json.load(f)

        current_balance=current_balance_list[-1]["amount"]
        latest_amount= {"id":current_user.id, "amount":current_balance-100}
        current_balance_list.append(latest_amount)
        with open('databases/bank.json', 'w') as fp:
            json.dump(current_balance_list, fp)
    
    return data, currency, positional_value

#4.2 WRITE USERLIST
def write_user():
    with open('databases/user_details.json') as f:
        initial_data = json.load(f)
    json_user_list = []

    for index,value in enumerate(initial_data):
        json_user_list.append(value["username"])

    with open('databases/user_list.json', 'w') as fp:
            json.dump(json_user_list, fp)

    return json_user_list

#5.ROUTING
@app.route('/')
def index():
    return render_template('index.html')

#5.1USER SIGNS-UP
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
        return redirect(url_for('login'))
    return render_template('signup.html',form=form)

#5.2.LOGIN APPLICATION
@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()  
        if user :
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('profile'))
        else :
            flash('Invalid username or password') 
    return render_template('login.html',form=form)

#5.3.VIEW PROFILE
@app.route('/profile',methods=['GET','POST'])
@login_required
def profile():
    #5.3.1.IMPLEMENT CUSTOM FUNCTION
    data, currency,x = find_current_user()
    return render_template('profile.html',data=data,currency=currency)

#5.4.SEND TOKENS
@app.route('/receive')
def receive():
    #5.4.1.IMPLEMENT CUSTOM FUNCTION
    data, currency, positional_value = find_current_user()

    #5.4.2.CREATE QR CODE FROM DATA
    username = data["username"]
    img=qrcode.make(data)
    img.save(f"static/pics/{username}_code.png")
    
    #5.3.3.LOAD QR CODE
    picture = os.path.join(app.config["UPLOAD_FOLDER"], f'{username}_code.png')

    return render_template('receive.html',data=data, picture=picture)


#5.5.RECEIVE TOKENS
@app.route('/send',methods=['GET','POST'])
def send():
    #5.5.1.IMPLEMENT CUSTOM FUNCTION
    data, currency, positional_value = find_current_user()
    user_list_data = write_user()
    user_list_data.remove(current_user.username)

    #5.5.2.IMPLEMENT CLASS
    form = TokeAmount()
    if form.validate_on_submit():
        user_balance = data["balance"]
        user_balance_typed =form.amount.data
        receiver = form.username.data
        receiver_data = "User does not exist"
         
        if user_balance_typed>user_balance:
             flash('You dont have that much tokens in your walet')

        else :
            #RECORD TRANSACTIONS
            with open('databases/user_details.json') as f:
                initial_data = json.load(f)
            isThere=False


            for x,y in enumerate(initial_data):
                if receiver==initial_data[x]["username"]:
                    y=initial_data[x]
                    isThere=True
                    position_value=x
                    receiver_data = y
            
            if isThere :
                #SUBTRACT AMOUNT FROM OWNER
                user_data, _,owner_position = find_current_user()
                subtracted_balance = user_data["balance"]-user_balance_typed
                user_data.update({"balance":subtracted_balance})
                initial_data[owner_position] = user_data
                
                #ADD AMOUNT TO RECEIVER
                added_balance = receiver_data["balance"]+user_balance_typed
                reciever_id = receiver_data["id"]
                receiver_data.update({"id":reciever_id,"username":receiver,"balance":added_balance})
                initial_data[position_value] = receiver_data
                print(initial_data)

                #EDIT JSON FILE
                with open('databases/user_details.json', 'w') as fp:
                    json.dump(initial_data, fp)

                flash(f"{user_balance_typed} ZA has been sent to {receiver}")
                
  
            else:
                
                print("data_user")
                
            #return render_template('profile.html',data=data,form=form)
    else:
        print("we don't have this")
  
    return render_template('send.html',data=data, form=form,user_list=user_list_data)

#5.6 CAPTURING IMAGE
@app.route('/capture', methods=['GET','POST'])
def capture():
    # if request.method == 'POST':
    #     return jsonify(request.form['file'])
    return render_template('capture.html', title='Upload a New Photo')

#LAST PART
@app.route('/logout')
@login_required
def logout():
    logout_user
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)