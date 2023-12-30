from flask import Blueprint, render_template, redirect, \
                flash, session
from datetime import datetime
import sys
sys.path.append('../')
from models.main import db
from models.user import User_Profile
from Forms.login_form import LoginForm
from Forms.signup_form import SignupForm

webpage_bp = Blueprint('webpage', __name__, template_folder='../../templates/Webpage')

# WEB-PAGE ROUTES
@webpage_bp.route('/test', methods=['GET', 'POST'])
def index():
    login_form = LoginForm()
    signup_form = SignupForm()

    if login_form.validate_on_submit():
        data = {k: v for k, v in login_form.data.items() if k != "csrf_token"}
        new_user = User_Profile(**data)
        return render_template('Homepage/home_page.html')
    else:
        return render_template('test.html', login_form=login_form, signup_form=signup_form)

@webpage_bp.route('/')
def still_show_landing_page():
    return redirect('/test')

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
def still_log_user_in():
    return redirect('/login/')

@webpage_bp.route('/register/', methods=['GET', 'POST'])
def register_new_user():
    form = SignupForm()
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
def still_register_new_user():
    return redirect('/register/')
