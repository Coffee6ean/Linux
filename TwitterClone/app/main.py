from flask import Flask, redirect, request, \
                render_template, session, flash
import os
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
import sys  
sys.path.append('../')
from models.main import db, connect_db
from models.user import User_Profile
from app.Forms.login_form import LoginForm
from app.Forms.signup_form import SignupForm
from app.Keys.secrets import APP_KEY

app = Flask(__name__, template_folder=template_dir)

app.app_context().push()        

# Configure the Flask app
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///twitter_clone_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'lol'
app.config['DEBUG_TB_INTERCEPTIONS_REDIRECTS'] = False

connect_db(app)

@app.route('/')
def landing_page():
    return render_template('Webpage/landing_page.html')

@app.route('/test', methods=['GET', 'POST'])
def index():
    login_form = LoginForm()
    signup_form = SignupForm()

    if login_form.validate_on_submit():
        data = {k: v for k, v in login_form.data.items() if k != "csrf_token"}
        new_user = User_Profile(**data)
        return render_template('test_success.html')
    else:
        return render_template('test.html', login_form=login_form, signup_form=signup_form)
