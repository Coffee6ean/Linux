from flask import Blueprint
import sys
sys.path.append('../')
from app.main import app, db, render_template, \
                    session, flash, redirect
from models.user import User_Profile, Board

main_bp = Blueprint('main_bp', __name__)
app.register_blueprint(main_bp)

# WEB-PAGE ROUTES
@main_bp.route('/')
def show_landing_page():
    return render_template('Webpage/landing_page.html') 

@main_bp.route('/login/', methods=['GET', 'POST'])
def log_user_in():
    form = LoginForm()
    if form.validate_on_submit():
        form_username = form.username.data
        form_password = form.password.data
        user = User_Profile.authenticate(username=form_username, password=form_password)

        if user:
            flash(f'Welcome back, {user.username}') 
            session['user_id'] = user.id
            return redirect('Homepage/home_page')
        else:
            flash('Invalid username/password. Please try again')
    return render_template('Webpage/user_login.html', form=form)

@main_bp.route('/login')
def log_user_in():
    return redirect('/login/')

@main_bp.route('/register/', methods=['GET', 'POST'])
def register_new_user():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        username = form.username.data
        password = form.password.data
        birth_date = birth_date
        new_user = User_Profile.register(
            email = email,
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
            birth_date = birth_date
        )
        db.session.add(new_user)

        try:    
            db.session.commit()
        except:
            form.username.errors.append('Username taken. Please pick another')
            return render_template('register.html', form=form)
        session['user_id'] = new_user.id
        flash(f'Welcome to the team, {new_user.username}')
        return render_template('User/user_profile', user=new_user)
    return render_template('Webpage/user_registration', form=form)

@main_bp.route('/register')
def register_new_user():
    return redirect('/register/')

# HOME-PAGE ROUTES
@main_bp.route('/home_page/')
def show_home_page():
    return render_template('Homepage/home_page.html')

@main_bp.route('/home_page')
def show_home_page():
    return redirect('/home_page/')

# USER ROUTES
@main_bp.route('/user/profile/')
def show_user_profile():
    user = User_Profile.query.get_or_404(session['user_id'])
    return render_template('User/user_profile.html', user=user)

@main_bp.route('/user/profile')
def show_user_profile():
    return redirect('/user/profile/')

@main_bp.route('/user/profile/', methods=['GET', 'POST'])
def delete_user_profile():
    user = User_Profile.query.get_or_404(session['user_id'])
    form = DeleteForm()
    if form.validate_on_submit():
        db.session.delete(user)
        db.session.commit()
        return redirect('/')

@main_bp.route('/user/<int:id>/')
def get_user_profile(id):   
    user = User_Profile.query.get_or_404(session['user_id'])
    if user:
        return render_template('User/user_profile.html', user=user)
    else:
        return render_template('404_page', user=user)
    
@main_bp.route('/user/<int:id>')
def get_user_profile():
    return redirect('/user/<int:id>/')

@main_bp.route('/user/posts/')
def get_user_posts():
    user = User_Profile.query.get_or_404(session['user_id'])
    all_user_posts = [post for post in user.posts]
    return render_template()
    
# BOARD ROUTES
@main_bp.route('/posts/')
def show_all_posts():
    boards = Board.query.all()
    return render_template('')