# WEB-PAGE ROUTES
@main_bp.route('/')
def landing_page():
    return render_template('landing_page.html') 

@main_bp.route('/login/', methods=['GET', 'POST'])
def user_login():
    form = UserForm()
    if form.validate_on_submit():
        form_username = form.username.data
        form_password = form.password.data
        user = User_Profile.authenticate(username=form_username, password=form_password)

        if user:
            flash(f'Welcome back, {user.username}')
            session['user_id'] = user.id
            return redirect('/home_page')
        else:
            flash('Invalid username/password. Please try again')
    return render_template('user_login.html', form=form)

@main_bp.route('/login')
def home_page():
    return redirect('/login/')