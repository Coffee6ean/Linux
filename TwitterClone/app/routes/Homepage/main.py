from flask import Blueprint, render_template, redirect, \
                flash, session
import sys
sys.path.append('../')
from models.user import User_Profile
from models.board import Board

homepage_bp = Blueprint('homepage', __name__, template_folder='../../templates/Homepage')

# HOME-PAGE ROUTES
@homepage_bp.route('/home_page/')
def show_home_page():
    return render_template('Homepage/home_page.html')

@homepage_bp.route('/home_page')
def still_show_home_page():
    return redirect('/home_page/')