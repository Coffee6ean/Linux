from flask import Blueprint, render_template, redirect, \
                flash, session
from datetime import datetime
import sys
sys.path.append('../')
from models.main import User_Profile

webpage_bp = Blueprint('webpage', __name__, template_folder='../../templates/Webpage')

# WEB-PAGE ROUTES
@webpage_bp.route('/')
def show_landing_page():
    return render_template('Webpage/landing_page.html') 

@webpage_bp.route('/login/', methods=['GET', 'POST'])
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

@webpage_bp.route('/login')
def log_user_in():
    return redirect('/login/')

@webpage_bp.route('/register/', methods=['GET', 'POST'])
def register_new_user():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        password = form.password.data
        birth_date_str = form.birth_date.data  # Received as a string
        birth_date = datetime.strptime(birth_date_str, '%m/%d/%Y').date()  # Convert to date type

        new_user = User_Profile.register(
            email = email,
            username = username,
            password = password,
            birth_date = datetime.strptime(birth_date).date()
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

@webpage_bp.route('/register')
def register_new_user():
    return redirect('/register/')
