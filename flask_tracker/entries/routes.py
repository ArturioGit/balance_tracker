from flask import Blueprint, url_for, redirect, abort, render_template, request
from flask_tracker.entries.forms import AddForm, EditEntryForm

from flask_tracker.entries.utils import (get_total, get_total_invest, get_total_invest_currency,
                                         get_total_сurrency, get_price)
from flask_tracker import db
from flask_tracker.models import Shopping, Currencies
from flask_login import current_user, login_required

entries = Blueprint('entries', __name__)


@entries.route('/tracking')
@login_required
def tracking():
    page = request.args.get("page", 1, type=int)
    entries_on_page = db.paginate(
        db.select(Shopping).filter_by(owner=current_user).order_by(Shopping.id.desc()), page=page, per_page=5)
    return render_template('tracking.html', entries_on_page=entries_on_page,
                           total_invest=get_total_invest(current_user), total_profit=get_total(current_user),
                           round=round)


@entries.route('/entries/<currency>')
@login_required
def entries_of_currency(currency):
    page = request.args.get("page", 1, type=int)
    entries_on_page = db.paginate(
        db.select(Shopping).filter_by(owner=current_user).filter_by(name=currency).order_by(Shopping.id.desc()),
        page=page, per_page=5)
    return render_template('currency_entries.html', entries_on_page=entries_on_page,
                           total_invest=get_total_invest_currency(current_user, currency),
                           total_profit=get_total_сurrency(current_user, currency),
                           get_price=get_price,
                           round=round, currency_name=currency)


@entries.route('/edit_entry/<int:entry_id>', methods=["POST", "GET"])
@login_required
def edit_entry(entry_id):
    entry = Shopping.query.get_or_404(entry_id)

    if entry.owner != current_user:
        abort(403)

    form = EditEntryForm()
    form.currency.choices = [(item.name, item.name) for item in Currencies.query.all()]
    if request.method != 'POST':
        form.currency.default = f'{entry.name}'
        form.price.default = entry.price
        form.amount.default = entry.amount_of_dollars
        form.process()

    if form.validate_on_submit():
        entry.name = form.currency.data
        entry.price = form.price.data
        entry.amount_of_dollars = form.amount.data
        db.session.commit()
        return redirect(url_for('entries.tracking'))

    return render_template('edit_entry.html', form=form, entry=entry)


@entries.route('/add_entry', methods=["POST", "GET"])
@login_required
def add_entry():
    form = AddForm()
    form.currency.choices = [(item.name, item.name) for item in Currencies.query.all()]
    if request.method != 'POST':
        currency_name = request.args.get('currency_name')
        form.currency.default = currency_name
        form.price.default = get_price(currency_name)
        form.amount.default = 1
        form.process()
    if form.validate_on_submit():
        shopping = Shopping(name=form.currency.data, price=form.price.data,
                            amount_of_dollars=form.amount.data, owner=current_user)
        db.session.add(shopping)
        db.session.commit()
        return redirect(url_for('entries.tracking'))
    return render_template('add_entry.html', form=form)


@entries.route('/delete_entry/<int:entry_id>', methods=["POST", "GET"])
@login_required
def delete_entry(entry_id):
    entry = Shopping.query.get_or_404(entry_id)
    if entry.owner != current_user:
        abort(403)
    db.session.delete(entry)
    db.session.commit()
    return redirect(url_for('entries.tracking'))
