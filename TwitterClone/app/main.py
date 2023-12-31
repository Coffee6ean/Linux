from flask import Flask, redirect, request, \
                render_template, session, flash
import os
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
import sys  
sys.path.append('../')
from models.main import db, connect_db
from models.user import User_Profile

# Forms 
from app.Forms.login_form import LoginForm
from app.Forms.signup_form import SignupForm

# Routes 
from app.routes.User.main import user_bp
from app.routes.Homepage.main import homepage_bp
from app.routes.Webpage.main import webpage_bp

# Key
from app.Keys.secrets import APP_KEY

app = Flask(__name__, template_folder=template_dir)

# Register blueprints
app.register_blueprint(webpage_bp)
app.register_blueprint(homepage_bp)
app.register_blueprint(user_bp)

app.app_context().push()        

# Configure the Flask app
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///twitter_clone_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = APP_KEY
app.config['DEBUG_TB_INTERCEPTIONS_REDIRECTS'] = False

connect_db(app)
