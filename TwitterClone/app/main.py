from flask import Flask, redirect, request, \
                render_template, session, flash
import os
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
import sys  
sys.path.append('../')
from models.main import db, connect_db
#from app.routes.Webpage.main import webpage_bp
#from app.routes.Homepage.main import homepage_bp
#from app.routes.User.main import user_bp
from app.Keys.secrets import APP_KEY

app = Flask(__name__, template_folder=template_dir)

app.app_context().push()        

# Configure the Flask app
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///auth_demo_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'lol'
app.config['DEBUG_TB_INTERCEPTIONS_REDIRECTS'] = False

#app.register_blueprint(homepage_bp)
#app.register_blueprint(user_bp)
#app.register_blueprint(webpage_bp)

connect_db(app)

@app.route('/')
def landing_page():
    return render_template('Webpage/landing_page.html')

@app.route('/login')
def login_page():
    return render_template('Webpage/user_login.html')

@app.route('/register')
def register_page():
    return render_template('Webpage/user_registration.html')