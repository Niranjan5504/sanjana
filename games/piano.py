# piano.py
from flask import Blueprint, render_template

# Define the Blueprint
piano_bp = Blueprint('piano', __name__, template_folder='templates')

# Define the route
@piano_bp.route('/piano')
def piano():
    return render_template('piano.html')
