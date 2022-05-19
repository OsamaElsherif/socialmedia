from enum import unique
from operator import countOf, pos
from re import L, S
import time
from flask.helpers import flash
from sqlalchemy.orm import backref
from scripts import tweeting, posting
from data import Twitter
from flask import Flask, render_template, url_for, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from functools import wraps
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
# from flask_login import LoginManager, login_user, logout_user, current_user
import ast
import twiiter
import facebook as fb
from selenium.webdriver.common.keys import Keys

# ---- intializations ----
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///socialmedia.db'
app.secret_key = 'testytestingtestful'
salt = b'\xec\x86\xc6\xcao?3`.\xe8\x86\x0b\xcd?I\x8dV\x808c\x94\x03\x95~\xf3\xb7<iV\xd9\xe1\x01'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
# login_manager = LoginManager(app)

# ---- consts ----
driver = object
accounts = { 
            'twitter' : 0,
            'facebook': 0
            }
connections = {}
new_tap = False

# ---- Functions ----
class current_user():
    def __init__(self):
        try:
            self.user = User.query.get(int(session['id']))
            print(self.user)
        except Exception as e:
            return None

    def user(self):
        return self.user

    def is_authenticated(self):
        try:
            if session['id'] and session['email'] and session['username']:
                return True
        except Exception as e:
            return False

class security():
    def __init__(self, user):
        self.user = user
        self.Secure_key = user.password

    def encrypt(self, e, p):
        email = bytes(e, 'utf-8')
        password = bytes(p, 'utf-8')

        General_key = PBKDF2(self.Secure_key, salt, dkLen=32)
        cipher = AES.new(General_key, AES.MODE_CBC)
        ciphered_email = cipher.encrypt(pad(email, AES.block_size))
        ciphered_password = cipher.encrypt(pad(password, AES.block_size))
        iv = cipher.iv

        data = {
            'email' : ciphered_email,
            'password' : ciphered_password,
            'iv' : iv
        }

        return data
    
    def decrypt(self, e, p, iv):
        E_email = e
        E_pass = p

        General_key = PBKDF2(self.Secure_key, salt, dkLen=32)
        cipher = AES.new(General_key, AES.MODE_CBC, iv=iv) 

        email = unpad(cipher.decrypt(E_email), AES.block_size)
        password =  unpad(cipher.decrypt(E_pass), AES.block_size)

        data = {
            'email' : email.decode('utf-8'),
            'password' : password.decode('utf-8')
        }

        return data
    
    def serialization(self, post):
        post = bytes(post, 'utf-8')
        General_key = PBKDF2(self.Secure_key, salt, dkLen=32)
        cipher = AES.new(General_key, AES.MODE_CBC)
        ciphered_post = cipher.encrypt(pad(post, AES.block_size))
        iv = cipher.iv
        i = Post.query.all()[-1].id
        data = {
            'id': i+1,
            'content': ciphered_post
        }
        post = Post(user=self.user.id, iv=iv)
        db.session.add(post)
        db.session.commit()
        return str(data)
    
    def deserilization(self, post):
        data = ast.literal_eval(post)
        id = data['id']
        content = data['content']

        iv = Post.query.get(id).iv

        General_key = PBKDF2(self.Secure_key, salt, dkLen=32)
        cipher = AES.new(General_key, AES.MODE_CBC, iv=iv) 

        post = unpad(cipher.decrypt(content), AES.block_size)

        return post.decode('utf-8')

class fetching():
    def __init__(self):
        pass
    
    def fetching_posts(self, account, driver, tap_handeling=True):
        if tap_handeling:
            tap_handel = connections[driver][account]['tap']
            driver.switch_to.window(tap_handel)
        souce = driver.page_source
        result = fb.scrapping(souce, 'profile', driver)
        return result
    
    def categorize(self, list_of_posts):
        categorized = {
            'encrypted' : [],
            'normal' : []
        }
        for post in list_of_posts:
            try:
                ast.literal_eval(post)
                categorized['encrypted'].append(post)
            except:
                categorized['normal'].append(post)
        
        return categorized
        

class sessions():
    def __init__(self, connections):
        self.connection = connections
        self.driver = object

    
    def create(self, driver):
        global connections
        connections[driver] = {}
    
    def add(self, type, driver, new_tap, window_handle):
        self.connection[driver][str(type)] = {}
        if new_tap:
            self.connection[driver][str(type)]['tap'] = window_handle
        else:
            self.connection[driver][str(type)]['tap'] = window_handle
        global connections
        connections = self.connection
    
    def show(self):
        global connections
        return connections


def login_user(user):
    session['id'] = user.id
    session['email'] = user.email
    session['username'] = user.username

    return 'logged in'

def logout_user():
    session.clear()

    return 'logged out'

# ---- Decorators ----

def loginrequired(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user().is_authenticated() is False:
            return redirect(url_for('login'))   
        return f(*args, **kwargs)
    return decorated_function

# ---- DATABASE -----
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(), nullable=False)
    lastname = db.Column(db.String(), nullable=False)
    username = db.Column(db.String(), nullable=False, unique=True)
    email = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    accounts = db.relationship('Account', backref='owner', lazy=True)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"USER('{self.username}', '{self.email}', '{self.password}')"

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.id') ,nullable=False)
    name = db.Column(db.String(), nullable=False) # Facebook, Twitter, etc.
    email = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    iv = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f"Account('{self.name}', '{self.userid}', '{self.iv}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    iv = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f"POSTS('{self.id}' , '{self.iv}')"

# ---- routes ----

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route('/timeline')
@loginrequired
def timeline():
    user = current_user().user
    users = User.query.all()
    user_accounts = user.accounts
    if connections:
        for connection in connections[driver]:
            driver.switch_to.window(connections[driver][connection]['tap'])
            if connection == 'facebook':
                driver.get('https://www.facebook.com')
            elif connection == 'twitter':
                driver.get('https://www.twitter.com')

    accounts_data = {}
    for account in user_accounts:
            accounts_data[account.name] = account
    print(sessions(connections).show())

    return render_template('index.html', accounts=accounts, user=user, accounts_data=accounts_data, users=users)
        

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user().is_authenticated():
        return redirect(url_for('timeline'))
    
    form = request.form
    if form:
        user = User.query.filter_by(email=form['email']).first()
        if user and bcrypt.check_password_hash(user.password, form['password']):
            login_user(user)
            return redirect(url_for('timeline'))
        else:
            flash("Your eamil or password are incorrect, please check your data and try again", "error")
            print("Your eamil or password are incorrect, please check your data and try again")

    return render_template('login.html')

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if current_user().is_authenticated():
        return redirect(url_for('timeline'))
    form = request.form
    if form:
        fname = form['fname']
        lname = form['lname']
        username = form['username']
        email = form['email']
        password = form['pass']
        repassword = form['repass']
        
        if password == repassword:
            hasehd_password = bcrypt.generate_password_hash(password).decode('utf-8')
            if User.query.filter_by(username=username).first():
                flash("This username is taken, please try another one", 'error')
            elif User.query.filter_by(email=email).first():
                flash("This email is already exist, have you forgot your password !")
            else:
                user = User(firstname=fname, lastname=lname, username=username, email=email, password=hasehd_password)
                db.session.add(user)
                db.session.commit()
                flash("Your account has been created successfully, you can now login", 'success')
                return redirect(url_for('login'))
        else:
            flash("Your password doesn't match, please check them", 'error')

    return render_template('signup.html')

@app.route('/forgot_password')
def forgot_password():
    if current_user().is_authenticated():
        return redirect(url_for('login'))
    return render_template('forgot_password.html')

@app.route('/share', methods=['POST'])
@loginrequired
def share():
    posting = request.form['posting']
    twitter = 0
    facebook = 0
    
    try:
        if request.form['t'] == 'on': twitter = 1
    except Exception as e:
        pass
    
    try:
        if request.form['f'] == 'on': facebook = 1
    except Exception as e:
        pass


    if twitter:
        tap_handle = connections[driver]['twitter']['tap']
        # driver.switch_to_window(driver.window_handles[tap_handle])
        driver.switch_to.window(tap_handle)
        tweet = security(current_user().user).serialization(posting)
        twiiter.tweet(driver, tweet)

    if facebook:
        tap_handle = connections[driver]['facebook']['tap']
        # driver.switch_to_window(driver.window_handles[tap_handle])
        driver.switch_to.window(tap_handle)
        post = security(current_user().user).serialization(posting)
        fb.post(driver, post)
    
    return redirect(url_for('timeline'))
    
    # return f"{posting} will be posted in {twitter} and {facebook}"

@app.route('/profile/<string:username>')
@loginrequired
def profile(username):
    user = current_user().user
    if username == user.username:
        result = fetching().fetching_posts('facebook', driver)
        print(result)
        categorized_result = fetching().categorize(result)
        encrypted_posts = categorized_result['encrypted']
        normal_posts = categorized_result['normal']
        for post in encrypted_posts:
            decrypted = security(user).deserilization(post)
            normal_posts.insert(0, decrypted)

        return render_template('profile.html', user=user, accounts=accounts, posts=normal_posts)
    else:
        user = User.query.filter_by(username=username).first()
        user_socials = user.accounts
        tempo_driver = object
        tempo_connected = {}
        for account in user_socials:
            print(account)
            if account.name == 'facebook':
                email = account.email
                password = account.password
                iv = account.iv
                res = security(user).decrypt(email, password, iv)
                if tempo_connected:
                    tempo_driver.get('https://www.facebook.com')
                    fb.login(tempo_driver, res['email'], res['password'])
                else:
                    tempo_driver = fb.intializtion()
                    tempo_connected[tempo_driver] = 1
                    fb.login(tempo_driver, res['email'], res['password'])

                result = fetching().fetching_posts('facebook', tempo_driver, tap_handeling=False)
                print(result)
                categorized_result = fetching().categorize(result)
                encrypted_posts = categorized_result['encrypted']
                normal_posts = categorized_result['normal']
                for post in encrypted_posts:
                    decrypted = security(user).deserilization(post)
                    normal_posts.insert(0, decrypted)
            # elif account.name == 'twitter':
            #     email = account.email
            #     password = account.password
            #     iv = account.iv
            #     res = security(user).decrypt(email, password, iv)
            #     if tempo_connected:
            #         tempo_driver.get('https://www.twitter.com/login')
            #         twiiter.login(tempo_driver, res['email'], res['password'])
            #     else:
            #         tempo_driver = twiiter.intializtion()
            #         tempo_connected[tempo_driver] = 1
            #         twiiter.login(tempo_driver, res['email'], res['password'])

        return render_template('profile.html', user=user, accounts=accounts, posts=normal_posts)

@app.route('/account/add', methods=['GET', 'POST'])
@loginrequired
def add_account():
    user = current_user().user
    form = request.form
    if form:
        name = form['account']
        email = form['email']
        password = form['password']
        res = security(user).encrypt(email, password)
        E_email = res['email']
        E_pass = res['password']
        iv = res['iv']
        # print(f"{str(E_email)} , {str(E_pass)} {str(iv)}")
        account = Account(userid=user.id, name=name, email=E_email, password=E_pass, iv=iv)
        db.session.add(account)
        db.session.commit()
    return render_template('add_account.html', accounts=accounts, user=user)

@app.route('/account/connect/<string:type>/<string:iv>')
def connect(type, iv):
    user = current_user().user
    user_accounts = user.accounts
    for account in user_accounts:
        if account.name == type:
            E_email = account.email
            E_password = account.password
            iv = account.iv

            res = security(user).decrypt(E_email, E_password, iv)

            global driver, accounts, new_tap
            
            if type == 'twitter':
                if connections:
                    driver.execute_script('''window.open("https://twitter.com/login","_blank");''')
                    driver.switch_to_window(driver.window_handles[-1])
                    new_tap = True
                else:
                    driver = twiiter.intializtion()
                response = twiiter.login(driver, res['email'], res['password'])
                if response == 'SUC::200':
                    if not new_tap:
                        sessions(connections).create(driver)
                    print(sessions(connections).add(type, driver, new_tap, driver.current_window_handle))
                    accounts['twitter'] = 1

            elif type == 'facebook':
                if connections:
                    driver.execute_script('''window.open("https://facebook.com","_blank");''')
                    driver.switch_to_window(driver.window_handles[-1])
                    new_tap = True
                else:
                    driver = fb.intializtion()
                response = fb.login(driver, res['email'], res['password'])
                # driver.switch_to.alert.dismiss()
                if response == 'SUC::200':
                    if not new_tap:
                        sessions(connections).create(driver)
                    print(sessions(connections).add(type, driver, new_tap, driver.current_window_handle))
                    accounts['facebook'] = 1


    return redirect(url_for('timeline'))

@app.route('/logout')
@loginrequired
def logout():
    logout_user()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True, host='192.168.1.6')