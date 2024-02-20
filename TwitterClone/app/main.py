from flask import Flask
from flask_cors import CORS  # Import CORS extension
import os
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
import sys  
sys.path.append('../')

# App Configuration
from config.app_config import DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS, DEBUG

# Models 
from models.main import db, connect_db

# Routes 
from app.routes.User.main import user_bp
from app.routes.Homepage.main import homepage_bp
from app.routes.Webpage.main import webpage_bp
from app.routes.Projects.main import project_bp

# Key
from app.Keys.secrets import APP_KEY

app = Flask(__name__, template_folder=template_dir)

# Apply CORS to your Flask app
CORS(app)

# Register blueprints
app.register_blueprint(webpage_bp)
app.register_blueprint(homepage_bp)
app.register_blueprint(user_bp)
app.register_blueprint(project_bp)

app.app_context().push()        

# Configure the Flask app
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = APP_KEY
app.config['DEBUG_TB_INTERCEPTIONS_REDIRECTS'] = DEBUG
app.config['WTF_CSRF_ENABLED'] = False

connect_db(app)
