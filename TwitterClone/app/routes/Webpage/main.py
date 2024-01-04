from flask import Blueprint, render_template, redirect, \
                flash, session, url_for
from datetime import datetime
import sys
sys.path.append('../')
from models.main import db
from models.user import User_Profile
from Forms.login_form import LoginForm
from Forms.signup_form import SignupForm

webpage_bp = Blueprint('webpage', __name__, template_folder='../../templates/Webpage/')

# WEB-PAGE ROUTES
@webpage_bp.route('/', methods=['GET', 'POST'])
def index():
    login_form = LoginForm()
    signup_form = SignupForm()
    
    return render_template('Webpage/landing_page.html', login_form=login_form, signup_form=signup_form)

@webpage_bp.route('/login', methods=['GET', 'POST'])
def log_user_in():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        form_email = login_form.email.data
        form_password = login_form.password.data
        user = User_Profile.authenticate(email=form_email, password=form_password)
        print('#################')
        print('User:', user)
        if user:
            flash(f'Welcome back, {user.username}!', 'success') 
            session['user_id'] = user.id
            return redirect(url_for('user.show_user_profile'))
        else:
            login_form.email.errors = ['Invalid username/password.']
    flash('Oops! Invalid username/password.', 'danger')
    return redirect('/')


@webpage_bp.route('/signup', methods=['GET', 'POST'])
def sign_user_up():
    signup_form = SignupForm()

    if signup_form.validate_on_submit():
        email = signup_form.email.data
        username = signup_form.username.data
        password = signup_form.password.data
        birth_date_str = signup_form.birth_date.data  # Received as a string
        birth_date = datetime.strptime(birth_date_str, '%m/%d/%Y').date()  # Convert to date type

        new_user = User_Profile.register(
            email = email,
            username = username,
            password = password,
            birth_date = birth_date
        )
        db.session.add(new_user)

        try:    
            db.session.commit()
        except:
            signup_form.username.errors.append('Username taken. Please pick another')
            return render_template('test.html', signup_form=signup_form)
        session['user_id'] = new_user.id
        flash(f'Welcome to the team, {new_user.username}!', 'success')
        return render_template('User/user_profile', user=new_user)
    return redirect('/')
