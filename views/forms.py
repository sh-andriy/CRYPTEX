from flask_wtf import FlaskForm
from wtforms import SubmitField, PasswordField, EmailField, SelectField, DecimalField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError


class RegistrationForm(FlaskForm):
    """
    A class that represents a user registration form.
    The form contains email, password, confirm password and submit fields

    Attributes:
        email(EmailField): an email input field;
        password(PasswordField): a password input field;
        confirm_password(PasswordField): a password confirmation field;
        submit(SubmitField): a submit button field with a label 'Sign Up'.
    """
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[DataRequired(), EqualTo('password')]
    )
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    """
    A class that represents a user login form.
    The form contains email, password and submit fields

    Attributes:
        email(EmailField): an email input field;
        password(PasswordField): a password input field;
        submit(SubmitField): a submit button field with a label 'Login'.
    """
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class BalanceForm(FlaskForm):
    """
    A class that represents form for creating a user balance.
    The form contains coin, amount and submit fields

    Attributes:
        coin(SelectField): cryptocurrency select field;
        amount(DecimalField): decimal amount input field;
        submit(SubmitField): a submit button field with a label 'Add'.
    """
    coin = SelectField('Coin', choices=[])
    amount = DecimalField('Amount', validators=[DataRequired()])
    submit = SubmitField('Add')

    def validate_amount(self, amount):
        """
        Function that validates balance amount added by a user.
        It checks if the number of digits after the decimal point is within the
        supported range and if the amount is within the allowed range. If the
        validation fails, a ValidationError is raised with an appropriate error message.

        Args:
            amount: The amount of a coin user wants to create a balance of.
        """
        try:  # pylint: disable=W0707
            digits_len = abs(amount.data.as_tuple().exponent)
            if digits_len > 7:
                raise ValueError("Sadly we only support only 7 values after comma")
            if amount.data > 100000 or amount.data < 0.0000001:
                raise ValueError("Sadly we only support values from range 0.0000001 to 100000")
        except ValueError as error:
            raise ValidationError(str(error)) from error
