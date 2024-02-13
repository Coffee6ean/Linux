# Flask Imports
from flask import Blueprint, render_template, redirect, \
                    flash, session, url_for, jsonify, abort, \
                    request

# System Imports
import sys

# Append Parent Directory to sys.path
sys.path.append('../')

# Database and Model Imports
from models.main import db
from models.user import User_Profile
from models.entity import Entity
from models.picture import Picture

# Form Imports
from forms.edit_form import EditForm
from forms.picture_form import PictureForm

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
    if 'username' in session:
        current_user = session['username']
        user = User_Profile.query.filter_by(username=username).first()

        if current_user == user.username:
            # User is viewing their own profile
            return render_template('User/user_profile.html', user=user, 
                                   version=APP_VERSION)
        else:
            # User is viewing someone else's profile
            return render_template('User/user_profile.html', user=user, 
                                   version=APP_VERSION)
    else:
        # Handle the case when the user is not in the session
        flash('User not logged in.', 'danger')
        return redirect(f'{BASE_ROUTE}/')

    
@user_bp.route(f'{USER_ROUTE}/<username>/edit')
def edit_user_profile(username):
    if username in session or username == session['username']:
        user = User_Profile.query.filter_by(username=username).first()
        edit_form = EditForm(obj=user)
        return render_template('User/edit_profile.html', edit_form=edit_form, 
                               user=user, version=APP_VERSION)
    else:
        # Handle the case when 'username' is not in the session
        return render_template('404_page.html')
    
@user_bp.route(f'{USER_ROUTE}/<username>/update', methods=['GET', 'POST'])
def update_user_profile(username):
    if username in session or username == session['username']:
        user = User_Profile.query.filter_by(username=username).first()
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
        return render_template('User/edit_profile.html', edit_form=edit_form, 
                               user=user, version=APP_VERSION)
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


#--- USER SECTIONS ---#
# Presentation Actions:
@user_bp.route(f'{USER_ROUTE}/<username>/presentation')
def display_user_presentation(username):
    user = User_Profile.query.filter_by(username=username).first()
    picture_form = PictureForm()

    if not user:
        abort(404)  # Abort with 404 error if user with the given username is not found

    return render_template('User/Sections/presentation.html', 
                           user=user, picture_form=picture_form, 
                           version=APP_VERSION)

@user_bp.route(f'{USER_ROUTE}/<username>/presentation/upload/picture', methods=['GET','POST'])
def upload_picture(username):
    # Make sure the current user is authorized to upload pictures
    current_user = User_Profile.query.get_or_404(session.get('user_id'))
    if current_user.username != username:
        flash("You are not authorized to upload pictures for this user.", "danger")
        return redirect(url_for('user.show_user_profile', username=username))

    picture_form = PictureForm()

    form_logger.print_form_debug_info(picture_form)
    form_logger.print_form_csrf_token(picture_form)
    if picture_form.validate_on_submit():
        try:
            image_file = picture_form.image.data
            description = picture_form.description.data
            picture = Picture(url=image_file, description=description, entity_id=current_user.id)

            db.session.add(picture)
            db.session.commit()

            flash("Picture uploaded successfully.", "success")
            return redirect(url_for('user.show_user_profile', username=username))
        except Exception as e:
            # Log the error
            #form_logger.error("An error occurred while uploading picture: %s", str(e))
            flash("Failed to upload picture. Please try again later.", "danger")
            db.session.rollback()  # Rollback the session to revert any changes
    else:
        form_logger.print_form_validation_failed(picture_form)
        flash("Failed to upload picture. Please check your inputs and try again.", "danger")

    return redirect(url_for('user.show_user_profile', username=username))

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

    user = User_Profile.query.filter_by(username=username).first()
    user_logger.print_user_serialization(user)

    return user.serialize()

@user_bp.route(f'{API_ROUTE}/protected-route')
def protected_route():
    username = session.get('username')
    print(username)

    if username:
        # Access user-specific data from the session
        user_data = User_Profile.query.filter_by(username=username).first()
        return jsonify({'message': 'Access granted', 
                        'user': user_data.username, 
                        'email': user_data.email})

    return jsonify({'message': 'Unauthorized'}), 401
