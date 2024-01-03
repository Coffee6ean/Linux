from flask import Blueprint, render_template, redirect, \
                flash, session
import sys
sys.path.append('../')
from models.user import User_Profile
from models.board import Board

user_bp = Blueprint('user', __name__, template_folder='../../templates/User/')

# USER ROUTES
@user_bp.route('/user/logout')
def logout_user():
    session.pop('user_id')
    flash('Successfully logged out', 'info')
    return redirect('/')

@user_bp.route('/user/profile')
def show_user_profile():
    if 'user_id' in session:
        user = User_Profile.query.get_or_404(session['user_id'])
        return render_template('User/user_profile.html', user=user)
    else:
        # Handle the case when 'user_id' is not in the session
        flash('User not logged in.')
        return redirect('/')

@user_bp.route('/user/profile/')
def still_show_user_profile():
    return redirect('/user/profile')

@user_bp.route('/user/profile', methods=['GET', 'POST'])
def delete_user_profile():
    user = User_Profile.query.get_or_404(session['user_id'])
    form = DeleteForm()
    if form.validate_on_submit():
        db.session.delete(user)
        db.session.commit()
        return redirect('/')

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

@user_bp.route('/user/<int:id>')
def get_user_profile(id):   
    user = User_Profile.query.get_or_404(id)
    if user:
        return render_template('user_profile.html', user=user)
    else:
        return render_template('404_page', user=user)
    
@user_bp.route('/user/<int:id>/')
def still_get_user_profile(id):
    return redirect(f'/user/{id}')

@user_bp.route('/user/posts')
def get_user_posts():
    user = User_Profile.query.get_or_404(session['user_id'])
    all_user_posts = [post for post in user.posts]
    return render_template()
    
# BOARD ROUTES
@user_bp.route('/posts')
def show_all_posts():
    boards = Board.query.all()
    return render_template('')