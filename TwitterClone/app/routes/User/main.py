from flask import Blueprint, render_template, redirect, \
                flash, session, url_for
import sys
sys.path.append('../')
from models.main import db
from models.user import User_Profile
from models.board import Board
from Forms.edit_form import EditForm

user_bp = Blueprint('user', __name__, template_folder=['../../templates/User/', '../../templates/'])

# USER ROUTES
@user_bp.route('/user/logout')
def logout_user():
    session.pop('username')
    flash('Successfully logged out', 'info')
    return redirect('/')

@user_bp.route('/user/<username>')
def show_user_profile(username):
    if 'username' in session:
        current_user = session['username']
        # Check if the current user is trying to view their own profile or another user's profile
        if current_user == username:
            user = User_Profile.query.get_or_404(username)
        else:
            user = User_Profile.query.get_or_404(username)
            # Add logic here if you want to restrict certain information for other users
        return render_template('User/user_profile.html', user=user)
    else:
        # Handle the case when user is not in the session
        flash('User not logged in.', 'danger')
        return redirect('/')
    
@user_bp.route('/user/<username>/edit')
def edit_user_profile(username):
    if username in session or username == session['username']:
        user = User_Profile.query.get_or_404(username)
        edit_form = EditForm(obj=user)
        return render_template('User/edit_profile.html', edit_form=edit_form, user=user)
    else:
        # Handle the case when 'username' is not in the session
        return render_template('404_page.html')
    
@user_bp.route('/user/<username>/update', methods=['GET', 'POST'])
def update_user_profile(username):
    if username in session or username == session['username']:
        user = User_Profile.query.get_or_404(username)
        edit_form = EditForm(obj=user)

        print('###################################')
        print('Form:', edit_form)
        print('Form Errors:', edit_form.errors)
        print('Form Validation:', edit_form.validate())
        print('###################################')
        if edit_form.validate_on_submit():
            # Populate the existing user object with form data
            edit_form.populate_obj(user)
            print('###################################')
            print(f'id: {user.id}')
            print(f'email: {user.email}')
            print(f'username: {user.username}')
            print(f'password: {user.password}')
            print(f'birth date: {user.birth_date}')
            print('###################################')
            
            db.session.commit()
            session['username'] = user.username
            flash('Profile updated successfully!', 'success')
            return redirect(f"/user/{user.username}")
        print('###################################')
        print('Form Validation Failed')
        print('Form Errors:', edit_form.errors)
        print('###################################')
        flash('Oppss! Something went wrong. Try again', 'danger')
        return render_template('User/edit_profile.html', edit_form=edit_form, user=user)
    else:
        # Handle the case when 'username' is not in the session
        return render_template('404_page.html')
   
@user_bp.route('/user/<username>/delete', methods=['POST'])
def delete_user_profile(username):
    """Remove user from app."""

    if "username" not in session or username != session['username']:
        return render_template('404_page.html')
    
    user = User_Profile.query.get_or_404(session['username'])
    db.session.delete(user)
    db.session.commit()
    session.pop('username')
    return redirect('/')

@user_bp.route('/user/posts')
def get_user_posts():
    user = User_Profile.query.get_or_404(session['username'])
    all_user_posts = [post for post in user.posts]
    return render_template()
    
@user_bp.route('/user/<username>/section')
def get_presentation():
    return render_template('User/Sections/presentation.html')

# User Profile - Sections
@user_bp.route('/user/presentation')
def presentation():
    return render_template('User/sections/presentation.html')

@user_bp.route('/user/recent_activity')
def recent_activity():
    return render_template('User/sections/recent_activity.html')

@user_bp.route('/user/recent_work')
def recent_work():
    return render_template('User/sections/recent_work.html')

@user_bp.route('/user/other')
def other():
    return render_template('User/sections/other.html')
