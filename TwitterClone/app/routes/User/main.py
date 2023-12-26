# USER ROUTES
@main_bp.route('/user/profile/')
def user_profile():
    user = User_Profile.query.get_or_404(session['user_id'])
    return render_template('user_profile.html', user=user)

@main_bp.route('/user/profile')
def home_page():
    return redirect('/user/profile/')

@main_bp.route('/user/profile/', methods=['GET', 'POST'])
def delete_profile():
    user = User_Profile.query.get_or_404(session['user_id'])
    form = DeleteForm()
    if form.validate_on_submit():
        db.session.remove(user)

@main_bp.route('/user/<int:id>/')
def get_user(id):   
    user = User_Profile.query.get_or_404(session['user_id'])
    if user:
        return render_template('user_profile.html', user=user)
    else:
        return render_template('404_page', user=user)
    
@main_bp.route('/user/<int:id>')
def home_page():
    return redirect('/user/<int:id>/')