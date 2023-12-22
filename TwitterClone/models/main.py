from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# ROUTES

# MODELS
# from board import Board
# from feedback import Feedback
# from post import Post
# from project import Project
# from user import User_Profile

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    """Connect to the DataBase."""
    db.app = app
    db.init_app(app)