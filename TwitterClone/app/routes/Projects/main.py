# Flask Imports
from flask import Blueprint, render_template, redirect, \
                    flash, session, url_for, jsonify, abort, \
                    request

# System Imports
import sys

# Append Parent Directory to sys.path
sys.path.append('../')

# Database and Model Imports
from models.main import db
from models.entity import Entity
from models.project import Project

# Form Imports
from forms.edit_form import EditForm
from forms.picture_form import PictureForm

# Configuration Imports
from config.app_config import APP_VERSION
from ..Webpage.main import BASE_ROUTE 

# Helper functions
from ..lib.Forms import reusable_methods as form_logger
from ..lib.User import reusable_methods as user_logger

# Constants for Routes
PROJECT_ROUTE = f'{BASE_ROUTE}/project'
API_ROUTE = '/api' + PROJECT_ROUTE

# Blueprint Initialization
project_bp = Blueprint('project', __name__, template_folder=[
    '../../templates/Projects/', 
    '../../templates/'
])


#--- PROJECT ROUTES ---#
@project_bp.route(f'{PROJECT_ROUTE}/excel-project')
def logout_user():
    return render_template('Projects/Excel/excel_form.html')