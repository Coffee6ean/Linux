# Flask Imports
from flask import Blueprint, render_template, redirect, \
                    flash, session, url_for, jsonify

# System Imports
import sys

# Append Parent Directory to sys.path
sys.path.append('../')

# Database and Model Imports
from models.main import db
from models.User.user import User_Profile
from models.board import Board

# Form Imports
from Forms.edit_form import EditForm

# Configuration Imports
from config.app_config import APP_VERSION
from ..Webpage.main import BASE_ROUTE 

# Helper functions
from ..lib.Forms import reusable_methods as form_logger
from ..lib.User import reusable_methods as user_logger

# Constants for Routes
USER_ROUTE = f'/{APP_VERSION}/user'
API_ROUTE = '/api' + USER_ROUTE

# Blueprint Initialization
user_bp = Blueprint('user', __name__, template_folder=[
    '../../templates/User/', 
    '../../templates/'
])


#--- USER ROUTES ---#
@user_bp.route(f'{USER_ROUTE}/logout')
def logout_user():
    session.pop('username')
    flash('Successfully logged out', 'info')
    return redirect(f'{BASE_ROUTE}/')

@user_bp.route(f'{USER_ROUTE}/<username>')
def show_user_profile(username):
    if 'user_id' in session:
        current_user_id = session['user_id']
        user = User_Profile.query.get_or_404(username)

        if current_user_id == user.id:
            # User is viewing their own profile
            return render_template('User/user_profile.html', user=user, version=APP_VERSION)
        else:
            # User is viewing someone else's profile
            return render_template('User/user_profile.html', user=user, version=APP_VERSION)
    else:
        # Handle the case when the user is not in the session
        flash('User not logged in.', 'danger')
        return redirect(f'{BASE_ROUTE}/')

    
@user_bp.route(f'{USER_ROUTE}/<username>/edit')
def edit_user_profile(username):
    if username in session or username == session['username']:
        user = User_Profile.query.get_or_404(username)
        edit_form = EditForm(obj=user)
        return render_template('User/edit_profile.html', edit_form=edit_form, user=user, version=APP_VERSION)
    else:
        # Handle the case when 'username' is not in the session
        return render_template('404_page.html')
    
@user_bp.route(f'{USER_ROUTE}/<username>/update', methods=['GET', 'POST'])
def update_user_profile(username):
    if username in session or username == session['username']:
        user = User_Profile.query.get_or_404(username)
        edit_form = EditForm(obj=user)
        form_logger.print_form_debug_info(edit_form)

        if edit_form.validate_on_submit():
            # Populate the existing user object with form data
            edit_form.populate_obj(user)
            user_logger.print_user_details(user)
            
            db.session.commit()
            session['username'] = user.username
            flash('Profile updated successfully!', 'success')
            return redirect(f"{USER_ROUTE}/{user.username}")
        
        form_logger.print_form_validation_failed(edit_form)
        flash('Oppss! Something went wrong. Try again', 'danger')
        return render_template('User/edit_profile.html', edit_form=edit_form, user=user, version=APP_VERSION)
    else:
        # Handle the case when 'username' is not in the session
        return render_template('404_page.html')
   
@user_bp.route(f'{USER_ROUTE}/<username>/delete', methods=['POST'])
def delete_user_profile(username):
    """Remove user from app."""

    if "username" not in session or username != session['username']:
        return render_template('404_page.html')
    
    user = User_Profile.query.get_or_404(session['username'])
    db.session.delete(user)
    db.session.commit()
    session.pop('username')
    return redirect(f'{BASE_ROUTE}/')

@user_bp.route(f'{USER_ROUTE}/posts')
def get_user_posts():
    user = User_Profile.query.get_or_404(session['username'])
    all_user_posts = [post for post in user.posts]
    return render_template()
    
@user_bp.route(f'{USER_ROUTE}/<username>/section')
def get_presentation():
    return render_template('User/Sections/presentation.html')

# User Profile - Sections
@user_bp.route(f'{USER_ROUTE}/<username>/presentation')
def presentation(username):
    user = User_Profile.query.get_or_404(username)

    return render_template('User/Sections/presentation.html', user=user)

@user_bp.route(f'{USER_ROUTE}/recent_activity')
def recent_activity():
    return render_template('User/sections/recent_activity.html')

@user_bp.route(f'{USER_ROUTE}/recent_work')
def recent_work():
    return render_template('User/sections/recent_work.html')

@user_bp.route(f'{USER_ROUTE}/other')
def other():
    return render_template('User/sections/other.html')

# USER API ROUTES
@user_bp.route(f'{API_ROUTE}/<username>')
def api_get_user_data(username):
    """Return basic info about user in JSON."""

    user = User_Profile.query.get_or_404(username)
    user_logger.print_user_serialization(user)

    return user.serialize()

@user_bp.route(f'{API_ROUTE}/protected-route')
def protected_route():
    username = session.get('username')
    print(username)

    if username:
        # Access user-specific data from the session
        user_data = User_Profile.query.get_or_404(username)
        return jsonify({'message': 'Access granted', 'user': user_data.username, 'email': user_data.email})

    return jsonify({'message': 'Unauthorized'}), 401
