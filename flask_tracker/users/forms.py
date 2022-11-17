from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional, ValidationError
from flask_tracker.models import User
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed
import re


class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2)])
    surname = StringField('Surname', validators=[DataRequired(), Length(min=2)])
    login = StringField('Login', validators=[DataRequired(), Length(min=2)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=1)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit')

    def validate_login(self, login):
        is_correct = re.findall(r'^[A-Za-z0-9_]+$', login.data)
        user = User.query.filter_by(login=login.data).first()
        if not is_correct:
            raise ValidationError('Do not use special characters')
        elif user:
            raise ValidationError('Such a login already exists')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Such an email already exists')


class LoginForm(FlaskForm):
    login = StringField('Login', validators=[DataRequired(), Length(min=1)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    remember = BooleanField('Remember')
    submit = SubmitField('Send')


class UpdateForm(FlaskForm):
    name = StringField('Name', validators=[Optional()])
    surname = StringField('Surname', validators=[Optional()])
    email = StringField('Email')
    avatar = FileField('Avatar', validators=[FileAllowed(['png', 'jpg']), Optional()])
    submit = SubmitField('Update')

    def validate_name(self, name):
        if name.data:
            if len(name.data) < 2:
                raise ValidationError('So short')

    def validate_surname(self, surname):
        if surname.data:
            if len(surname.data) < 2:
                raise ValidationError('So short')

    def validate_email(self, email):
        if email.data != current_user.email and email.data:
            if not re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email.data):
                raise ValidationError('Invalid Email')
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Such an email already exists')


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=1)])
    submit = SubmitField('Request reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset password')
