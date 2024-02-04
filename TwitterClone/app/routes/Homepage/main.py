# Flask Imports
from flask import Blueprint, render_template, redirect, flash, session

# System Imports
import sys

# Append Parent Directory to sys.path
sys.path.append('../')

# Model Imports
from models.User.user import User_Profile
from models.post import Post
from models.board import Board

# Configuration Imports
from config.app_config import APP_VERSION
from ..Webpage.main import BASE_ROUTE 

# Blueprint Initialization
homepage_bp = Blueprint('homepage', __name__, template_folder='../../templates/Homepage')


# HOME-PAGE ROUTES
@homepage_bp.route(f'{BASE_ROUTE}/home_page')
def show_home_page():
    return render_template('Homepage/home_page.html', version=APP_VERSION)

# POSTS ROUTES
@homepage_bp.route(f'{BASE_ROUTE}/posts')
def show_all_posts():
    posts = Post.query.all()
    return render_template('Homepage/Posts/all_posts.html', posts=posts, version=APP_VERSION)

# ALL USERS ROUTES
@homepage_bp.route(f'{BASE_ROUTE}/user/all')
def show_all_users():
    users = User_Profile.query.all()
    return render_template('Homepage/all_users.html', users=users, version=APP_VERSION)
