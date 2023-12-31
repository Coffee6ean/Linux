from flask import Blueprint, render_template, redirect, \
                flash, session
import sys
sys.path.append('../')
from models.user import User_Profile
from models.post import Post
from models.board import Board

homepage_bp = Blueprint('homepage', __name__, template_folder='../../templates/Homepage')

# HOME-PAGE ROUTES
@homepage_bp.route('/home_page')
def show_home_page():
    return render_template('Homepage/home_page.html')

# POSTS ROUTES
@homepage_bp.route('/posts')
def show_all_posts():
    posts = Post.query.all()
    return render_template('Homepage/all_posts.html', posts=posts)

# ALL USERS ROUTES
@homepage_bp.route('/users')
def show_all_users():
    users = User_Profile.query.all()
    return render_template('Homepage/all_users.html', users=users)
