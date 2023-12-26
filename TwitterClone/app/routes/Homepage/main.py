# HOME-PAGE ROUTES
@main_bp.route('/home_page/')
def home_page():
    return render_template('home_page.html')

@main_bp.route('/home_page')
def home_page():
    return redirect('/home_page/')