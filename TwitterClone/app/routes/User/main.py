from flask import Blueprint, render_template, redirect, \
                flash, session
import sys
sys.path.append('../')
from models.main import User_Profile, Board

user_bp = Blueprint('user', __name__, template_folder='../../templates/User')

# USER ROUTES
@user_bp.route('/user/profile/')
def show_user_profile():
    user = User_Profile.query.get_or_404(session['user_id'])
    return render_template('User/user_profile.html', user=user)

@user_bp.route('/user/profile')
def show_user_profile():
    return redirect('/user/profile/')

@user_bp.route('/user/profile/', methods=['GET', 'POST'])
def delete_user_profile():
    user = User_Profile.query.get_or_404(session['user_id'])
    form = DeleteForm()
    if form.validate_on_submit():
        db.session.delete(user)
        db.session.commit()
        return redirect('/')

@user_bp.route('/user/<int:id>/')
def get_user_profile(id):   
    user = User_Profile.query.get_or_404(session['user_id'])
    if user:
        return render_template('User/user_profile.html', user=user)
    else:
        return render_template('404_page', user=user)
    
@user_bp.route('/user/<int:id>')
def get_user_profile():
    return redirect('/user/<int:id>/')

@user_bp.route('/user/posts/')
def get_user_posts():
    user = User_Profile.query.get_or_404(session['user_id'])
    all_user_posts = [post for post in user.posts]
    return render_template()
    
# BOARD ROUTES
@user_bp.route('/posts/')
def show_all_posts():
    boards = Board.query.all()
    return render_template('')