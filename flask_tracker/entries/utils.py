import requests
from flask_tracker import db
from flask_tracker.models import Shopping
from flask_login import current_user

key = "https://api.binance.com/api/v3/ticker/price?symbol="
value = 'BTC'


def get_price(currency):
    return requests.get(key + currency + 'USDT').json()['price']


def get_total(user):
    entries_on_page = db.session.execute(
        db.select(Shopping).filter_by(owner=user)).scalars().all()
    total_sum = 0
    for entries in entries_on_page:
        amount = (float(entries.amount_of_dollars) / float(entries.price)) * float(get_price(entries.name))
        total_sum += amount
    return round(total_sum, 4)


def get_total_invest(user):
    entries_on_page = db.session.execute(
        db.select(db.func.sum(Shopping.amount_of_dollars)).filter_by(owner=user)).scalars().first()
    return entries_on_page


def get_total_сurrency(user, name):
    entries_on_page = db.session.execute(
        db.select(Shopping).filter_by(owner=user).filter_by(name=name)).scalars().all()
    total_sum = 0
    for entries in entries_on_page:
        amount = (float(entries.amount_of_dollars) / float(entries.price)) * float(get_price(entries.name))
        total_sum += amount
    return round(total_sum, 4)


def get_total_invest_currency(user, name):
    entries_on_page = db.session.execute(
        db.select(db.func.sum(Shopping.amount_of_dollars)).filter_by(owner=user).filter_by(name=name)).scalars().first()
    return entries_on_page
