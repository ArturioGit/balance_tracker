from flask import Blueprint, render_template, url_for, flash, redirect
from flask_tracker.models import User
from flask_tracker.users.forms import (RegistrationForm, LoginForm, UpdateForm, RequestResetForm,
                                       ResetPasswordForm)
from flask_tracker import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, logout_user
from flask_tracker.users.utils import save_avatar, send_reset_email

users = Blueprint('users', __name__)


@users.route('/login', methods=["POST", "GET"])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('users.profile', id='good'))
    if form.validate_on_submit():
        user = User.query.filter_by(login=form.login.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('users.profile', id='good'))
        else:
            flash('Login unsuccessful', 'error')
    return render_template('login.html', form=form)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('users.login'))


@users.route('/registration', methods=["POST", "GET"])
def registration():
    form = RegistrationForm()
    if current_user.is_authenticated:
        return redirect(url_for('users.profile'))
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(name=form.name.data, surname=form.surname.data, login=form.login.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('The account was created', 'success')
        return redirect(url_for('users.profile'))
    return render_template('registration.html', form=form)


@users.route('/profile', methods=["POST", "GET"])
@login_required
def profile():
    form = UpdateForm()
    file = url_for('static', filename=f'img/avatars/{current_user.avatar}')
    if form.validate_on_submit():
        if form.surname.data:
            current_user.surname = form.surname.data
        if form.name.data:
            current_user.name = form.name.data
        if form.email.data:
            current_user.email = form.email.data
        if form.avatar.data:
            avatar_filename = save_avatar(form.avatar.data)
            current_user.avatar = avatar_filename
        db.session.commit()
        return redirect(url_for('users.profile'))

    return render_template('profile.html', file=file, form=form)


@users.route('/request_reset', methods=["POST", "GET"])
def request_reset():
    if current_user.is_authenticated:
        return redirect(url_for('users.profile'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('Instruction has sent on your email', 'info')
        return redirect(url_for('users.login'))
    return render_template('request_reset.html', form=form)


@users.route('/reset_password/<token>', methods=["POST", "GET"])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('users.profile'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('It is invalid or expired token', 'error')
        return redirect(url_for('users.request_reset'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user.password = hashed_password
        db.session.commit()
        flash('Password has been updated', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_password.html', form=form)
