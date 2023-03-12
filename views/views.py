import requests
from flask import (
    render_template,
    flash,
    Blueprint,
    redirect,
    request,
    url_for,
    current_app,
)
from flask_login import login_user, login_required, logout_user, current_user

from views.forms import RegistrationForm, LoginForm, BalanceForm
from models import Balance
from service import login_manager, CustomUser


blueprint = Blueprint('blueprint', __name__)


@login_manager.user_loader
def load_user(user_url):
    """
    This function is used by Flask-Login to load the current user object from the user ID that
    is stored in the session. This function takes a user URL as an argument and returns a
    CustomUser object that is created by calling the create_from_api class method of the
    CustomUser class.

    Args:
    user_url(str): The URL of the current user.

    Returns:
    CustomUser: A CustomUser object representing the current user.
    """
    return CustomUser.create_from_api(user_url)


@blueprint.route('/', methods=['GET', 'POST'])
def home():
    """
    Function that renders the home page of the application.

    If the user is authenticated, this function retrieves the balances of the user
    from the API, according to the dates selected by the user in the search form.
    The balances are displayed in a table in the template.

    Returns:
        A rendered template ('home.html') with the following context variables:
            - from_date: A string with the 'from' date selected by the user.
            - to_date: A string with the 'to' date selected by the user.
            - balances: A list of dictionaries with the balances of the user.

        Each dictionary contains the following keys:
            * coin_abbreviation: A string with the abbreviation of the coin.
            * amount: A float with the amount of the coin in the balance.
            * value: A float with the value of the coin in the balance, in USD.

    """
    current_app.logger.info("VIEW - Request from user - home page")
    from_date = request.form.get('from-date')
    to_date = request.form.get('to-date')
    context = {
        "from_date": from_date,
        "to_date": to_date,
    }
    current_app.logger.info(f"VIEW - Filters {context}")
    if current_user.is_authenticated:
        current_app.logger.info("VIEW - Balance search start")
        response = requests.get(
            timeout=5,
            url=f'{request.url_root}api/v1/balances/{current_user.id}',
            json={
                "from_date": from_date,
                "to_date": to_date,
            }
        )
        if response.status_code == 200:
            context['balances'] = response.json()
            current_app.logger.info(f"VIEW - Balances found: '{len(context['balances'])}'")
        current_app.logger.info("VIEW - Balance search end")
    return render_template('home.html', context=context)


@blueprint.route('/add-balance', methods=['GET', 'POST'])
@login_required
def add_balance():
    """
    Function that renders a form for user to add balance for a specific coin(crypto).

    Returns:
        If form submission is valid and API response status code is 201, then redirects to home page
        Otherwise, re-renders the same form with error message.

    """
    form = BalanceForm()

    coins = requests.get(url=f'{request.url_root}api/v1/coins', timeout=5)

    if coins.status_code == 200:
        available_coins = [
            (coin['id'], coin['abbreviation'])
            for coin in coins.json()
        ]
        form.coin.choices = available_coins

    if form.validate_on_submit():
        current_app.logger.info("VIEW - Add Balance request started")
        response = requests.post(
            timeout=5,
            url=f'{request.url_root}api/v1/balances',
            json={
                'user_id': current_user.id,
                'coin_id': int(form.coin.data),
                'amount': str(form.amount.data)
            }
        )
        if response.status_code == 201:
            flash('Coin Added Successfully!')
            current_app.logger.info("VIEW - Add Balance successful")
            current_app.logger.info("VIEW - Add Balance request ended")
            return redirect(url_for('blueprint.home'))
        current_app.logger.info("VIEW - Add Balance request failed")
        flash('Something went wrong, please try again!')
    return render_template('balance.html', form=form)


@blueprint.route('/edit-balance/<int:balance_id>', methods=['GET', 'POST', 'PUT'])
@login_required
def edit_balance(balance_id):
    """
    Function that renders the edit balance page and allows users to
    update their balance information.

    Args:
        balance_id: integer representing the id of the balance to be edited.

    Returns:
        If the balance is successfully updated, the function redirects
        the user to the home page with a success message.

        If there's an error, the function redirects
        the user to the edit balance page with an error message.
    """
    form = BalanceForm()
    balance = Balance.query.get(balance_id)
    coins = requests.get(url=f'{request.url_root}api/v1/coins', timeout=5)

    if coins.status_code == 200:
        available_coins = [
            (coin['id'], coin['abbreviation'])
            for coin in coins.json()
        ]
        form.coin.choices = available_coins

    if form.validate_on_submit():
        current_app.logger.info("VIEW - Edit Balance request started")
        response = requests.put(
            timeout=5,
            url=f'{request.url_root}api/v1/balances/{balance_id}',
            json={
                'coin_id': int(form.coin.data),
                'amount': str(form.amount.data)
            }
        )
        if response.status_code == 201:
            flash('Balance Updated Successfully!')
            current_app.logger.info(f"VIEW - Edit Balance with"
                                    f" id '{balance.id}' - updated successfully")
            current_app.logger.info("VIEW - Edit Balance request ended")
            return redirect(url_for('blueprint.home'))
        current_app.logger.info("VIEW - Edit Balance request failed")
        flash('Sorry, something went wrong :( Try again...')
    form.coin.data = balance.coin_id
    form.amount.data = balance.amount
    return render_template('edit_balance.html', form=form, balance=balance)


@blueprint.route('/delete-balance/<int:balance_id>', methods=['GET', 'POST'])
@login_required
def delete_balance(balance_id: int):
    """
    Function that handles deleting a balance for a logged-in user.

    Args:
        balance_id(int): The ID of the balance to be deleted.

    Returns:
        redirect: Redirects to the home page after the balance has been deleted.
    """
    response = requests.delete(
        timeout=5,
        url=f'{request.url_root}api/v1/balances/{balance_id}'
    )
    if response.status_code == 204:
        current_app.logger.info("VIEW - Balance delete successful")
        flash("Balance deleted")

    return redirect(url_for('blueprint.home'))


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    """
    Function that renders a register page for users to register
    into the application.
    If the user submits valid credentials, they are registered,
    logged in and redirected to the home page.

    If the credentials are invalid, an error message is displayed
    and the login page is re-rendered.

    Returns:
        If the request method is GET, returns a rendered register
        template with a sign-up form.
        If the request method is POST and the form is valid, registers,
        logs in the user and redirects them to the home page.
        If the request method is POST and the form is invalid, returns
        a rendered register template with error messages.
    """
    form = RegistrationForm()
    email = form.email.data
    if form.validate_on_submit():
        current_app.logger.info("VIEW - Register request started")
        response = requests.post(
            timeout=5,
            url=f'{request.url_root}api/v1/users',
            json={'email': form.email.data, 'password': form.password.data}
        )
        if response.status_code in [200, 201]:
            flash('User Registered Successfully!')
            login_user(CustomUser.create_from_api(response.headers.get('Location')))
            current_app.logger.info(f"VIEW - User with "
                                    f"id '{current_user.id}' - registered successfully")
            current_app.logger.info("VIEW - Register request ended")
            return redirect(url_for('blueprint.home'))
        current_app.logger.info("VIEW - Register request failed")
        flash('Something went wrong!')
    return render_template('register.html', form=form, email=email)


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    """
    Function that renders a login page for users to logs-in
    into the application.
    If the user submits valid credentials, they are logged in
    and redirected to the home page.
    If the credentials are invalid, an error message is displayed
    and the login page is re-rendered.

    Returns:
        If the request method is GET, returns a rendered login
         template with a login form.
        If the request method is POST and the form is valid,
         logs in the user and redirects them to the home page.
        If the request method is POST and the form is invalid,
         returns a rendered login template with error messages.
    """
    form = LoginForm()
    if form.validate_on_submit():
        current_app.logger.info("VIEW - Login request started")
        response = requests.post(
            timeout=5,
            url=f'{request.url_root}api/v1/users',
            json={'email': form.email.data, 'password': form.password.data}
        )
        if response.status_code == 200:
            flash('User Logged Successfully!')
            login_user(CustomUser.create_from_api(response.headers.get('Location')))

            current_app.logger.info(f"VIEW - User with id '{current_user.id}' - login successfully")
            current_app.logger.info("VIEW - Login request ended")

            return redirect(url_for('blueprint.home'))

        current_app.logger.info("VIEW - Login request failed")
        flash('Sorry, Wrong Credentials! Try Again...')

    return render_template('login.html', form=form)


@blueprint.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    """
    A function that logs out current user and flashes you a message using Flask flash.

    Returns:
        redirects you to a home page
    """
    current_app.logger.info("VIEW - User logout successfully")
    logout_user()
    flash('You have been logout successfully!', 'success')
    return redirect(url_for('blueprint.home'))
