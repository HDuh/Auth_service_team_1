from flask import Blueprint, render_template
from app.core.db import db

main = Blueprint('main', __name__)


@main.route('/')
def main_page():
    return render_template('main_page.html')


@main.route('/profile')
def profile():
    return render_template('profile.html')
