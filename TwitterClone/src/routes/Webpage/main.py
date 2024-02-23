# Flask Imports
from flask import Blueprint, render_template, redirect, \
                flash, session, url_for, request
from datetime import datetime

# System Imports
import sys

# Append Parent Directory to sys.path
sys.path.append('../')

# Database and Model Imports
from models.main import db
from models.user import User_Profile

# Form Imports
from forms.login_form import LoginForm
from forms.signup_form import SignupForm

# Configuration Imports
from config.app_config import APP_VERSION

# Helper functions
from ..lib.Forms import reusable_methods as form_logger
from ..lib.User import reusable_methods as user_logger

# Constants for Routes
BASE_ROUTE = f'/{APP_VERSION}'

# Blueprint Initialization
webpage_bp = Blueprint('webpage', __name__, template_folder=[
    '../../templates/Webpage/', 
    '../../templates/'
])


#--- WEB-PAGE ROUTES ---#
@webpage_bp.route('/')
def auto_redirect():
    return redirect(url_for('webpage.index'))

@webpage_bp.route(f'{BASE_ROUTE}/', methods=['GET', 'POST'])
def index():
    login_form = LoginForm()
    signup_form = SignupForm()
    
    return render_template('Webpage/landing_page.html', login_form=login_form, signup_form=signup_form, version=APP_VERSION)

@webpage_bp.route(f'{BASE_ROUTE}/login', methods=['GET', 'POST'])
def log_user_in():
    login_form = LoginForm()

    form_logger.print_form_debug_info(login_form)
    form_logger.print_form_csrf_token(login_form)
    if login_form.validate_on_submit():
        form_email = login_form.email.data
        form_password = login_form.password.data
        user = User_Profile.authenticate(email=form_email, password=form_password)

        if user:
            user_logger.print_user_details(user)
            flash(f'Welcome back, {user.username}!', 'success') 
            session['username'] = user.username
            session['user_id'] = user.id
            return redirect(f"{BASE_ROUTE}/user/{user.username}")
        else:
            login_form.email.errors = ['Invalid username/password.']
    form_logger.print_form_validation_failed(login_form)
    flash('Oops! Invalid username/password.', 'danger')
    return redirect(f'{BASE_ROUTE}/')

@webpage_bp.route(f'{BASE_ROUTE}/signup', methods=['GET', 'POST'])
def sign_user_up():
    signup_form = SignupForm()

    form_logger.print_form_debug_info(signup_form)
    form_logger.print_form_csrf_token(signup_form)
    if signup_form.validate_on_submit():
        form_email = signup_form.email.data
        form_username = signup_form.username.data
        form_password = signup_form.password.data
        birth_date_str = signup_form.birth_date.data  # Received as a string
        form_birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date()  # Convert to date type

        new_user = User_Profile.register(
            form_email, form_username, form_password, form_birth_date
        )
        user_logger.print_user_details(new_user)
  
        db.session.commit()
        session['username'] = new_user.username
        session['user_id'] = new_user.id
        flash(f'Welcome to the team, {new_user.username}!', 'success')
        return redirect(f"{BASE_ROUTE}/user/{new_user.username}")
    else:
        form_logger.print_form_validation_failed(signup_form)
        flash('Email/Username taken. Please pick another', 'danger')
        return redirect(f'{BASE_ROUTE}/')

@webpage_bp.route(f'{BASE_ROUTE}/register', methods=['GET', 'POST'])
def register():
    """Register a user: handle form submission."""

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        birth_date = request.form['birthdate']
        form_birth_date = datetime.strptime(birth_date, '%Y-%m-%d').date()

        new_user = User_Profile.register(email, username, password, form_birth_date)

        try:
            db.session.commit()
        except:
            flash('Username/Email taken. Please pick another', 'danger')
            return redirect(f'{BASE_ROUTE}/')
        session['username'] = new_user.username
        flash(f'Welcome to the team, {new_user.username}!', 'success')
        return redirect(f"{BASE_ROUTE}/user/{new_user.username}")

    return render_template('register_template.html', version=APP_VERSION)
