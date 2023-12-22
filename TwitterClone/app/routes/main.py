from flask import Blueprint
import sys
sys.path.append('../')
from app.main import app, render_template

main_bp = Blueprint('main_bp', __name__)
app.register_blueprint(main_bp)

@main_bp.route('/')
def landing_page():
    return render_template('landing_page.html') 
            