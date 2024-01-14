from flask import Blueprint, render_template, redirect, \
                flash, session, url_for, request
from datetime import datetime
import sys
sys.path.append('../')
from models.main import db
from models.user import User_Profile
from Forms.login_form import LoginForm
from Forms.signup_form import SignupForm
from Forms.register_form import RegisterForm

webpage_bp = Blueprint('webpage', __name__, template_folder=['../../templates/Webpage/', '../../templates/'])

# WEB-PAGE ROUTES
@webpage_bp.route('/', methods=['GET', 'POST'])
def index():
    login_form = LoginForm()
    signup_form = SignupForm()
    register_form = RegisterForm()
    
    return render_template('Webpage/landing_page.html', login_form=login_form, signup_form=signup_form)

@webpage_bp.route('/login', methods=['GET', 'POST'])
def log_user_in():
    login_form = LoginForm()

    print('###################################')
    print('Form:', login_form)
    print('Form Errors:', login_form.errors)
    print('Form Validation:', login_form.validate_on_submit())
    print('###################################')
    if login_form.validate_on_submit():
        form_email = login_form.email.data
        form_password = login_form.password.data
        user = User_Profile.authenticate(email=form_email, password=form_password)
        print('###################################')
        print(f'id: {user.id}')
        print(f'email: {user.email}')
        print(f'username: {user.username}')
        print(f'password: {user.password}')
        print(f'birth date: {user.birth_date}')
        print('###################################')
        if user:
            flash(f'Welcome back, {user.username}!', 'success') 
            session['username'] = user.username
            return redirect(f"/user/{user.username}")
        else:
            login_form.email.errors = ['Invalid username/password.']
    flash('Oops! Invalid username/password.', 'danger')
    return redirect('/')


@webpage_bp.route('/signup', methods=['GET', 'POST'])
def sign_user_up():
    signup_form = SignupForm()

    print('###################################')
    print('Form:', signup_form)
    print('Form Errors:', signup_form.errors)
    print('Form Validation:', signup_form.validate_on_submit())
    print('###################################')
    if signup_form.validate_on_submit():
        form_email = signup_form.email.data
        form_username = signup_form.username.data
        form_password = signup_form.password.data
        birth_date_str = signup_form.birth_date.data  # Received as a string
        form_birth_date = datetime.strptime(birth_date_str, '%m/%d/%Y').date()  # Convert to date type

        new_user = User_Profile.register(
            form_email, form_username, form_password, form_birth_date
        )
        print('###################################')
        print(f'id: {new_user.id}')
        print(f'email: {new_user.email}')        
        print(f'username: {new_user.username}')     
        print(f'password: {new_user.password}')     
        print(f'birth date: {new_user.birth_date}')   
        print('###################################')
  
        db.session.commit()
        session['username'] = new_user.username
        flash(f'Welcome to the team, {new_user.username}!', 'success')
        return redirect(f"/user/{new_user.username}")
    else:
        flash('Email/Username taken. Please pick another', 'danger')
        return redirect('/') 
        #return render_template('Webpage/landing_page.html', signup_form=signup_form)

@webpage_bp.route('/register', methods=['GET', 'POST'])
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
            return redirect('/')
        session['username'] = new_user.username
        flash(f'Welcome to the team, {new_user.username}!', 'success')
        return redirect(f"/user/{new_user.username}")

    return render_template('register_template.html')
