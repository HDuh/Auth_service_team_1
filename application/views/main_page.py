from flask import Blueprint, render_template
from flask_login import login_required, current_user

main = Blueprint('main', __name__)


@main.route('/')
def main_page():
    return render_template('main_page.html')


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.email)
