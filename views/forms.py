import requests
from decimal import Decimal

from flask import request
from flask_wtf import FlaskForm
from wtforms import SubmitField, PasswordField, EmailField, FloatField, SelectField, DecimalField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, NumberRange


class RegistrationForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class BalanceForm(FlaskForm):
    coin = SelectField('Coin', choices=[])
    amount = DecimalField('Amount', validators=[DataRequired()])
    submit = SubmitField('Add')

    def validate_amount(self, amount):
        try:
            digits_len = abs(amount.data.as_tuple().exponent)
            if digits_len > 7:
                raise ValueError("Sadly we only support only 7 values after comma")
            if amount.data > 100000 or amount.data < 0.0000001:
                raise ValueError("Sadly we only support values from range 0.0000001 to 100000")
        except ValueError as error:
            raise ValidationError(str(error))
