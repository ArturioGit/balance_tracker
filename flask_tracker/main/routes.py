from flask import Blueprint, render_template
from flask_tracker.models import Currencies

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    return render_template('index.html')


@main.route('/projects')
def projects():
    list_of_currencies = Currencies.query.all()
    return render_template('projects.html', list_of_currencies=list_of_currencies)
