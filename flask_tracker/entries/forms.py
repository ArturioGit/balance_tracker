from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, FloatField
from wtforms.validators import DataRequired


class AddForm(FlaskForm):
    currency = SelectField('Currency', choices=[], coerce=str, default='')
    price = FloatField('Price', validators=[DataRequired()])
    amount = FloatField('Amount USDT', validators=[DataRequired()])
    submit = SubmitField('Add')


class EditEntryForm(FlaskForm):
    currency = SelectField('Currency', choices=[])
    price = FloatField('Price', validators=[DataRequired()])
    amount = FloatField('Amount USDT', validators=[DataRequired()])
    submit = SubmitField('Edit')
