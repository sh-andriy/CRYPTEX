from views.forms import RegistrationForm, LoginForm, BalanceForm
from models import User
from service import login_manager
from models import db
import requests

from flask import (
    render_template,
    flash,
    Blueprint,
    redirect,
    request,
    url_for,
    session
)
from service import CustomUser
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

blueprint = Blueprint('blueprint', __name__)


@login_manager.user_loader
def load_user(user_url):
    return CustomUser.create_from_api(user_url)


@blueprint.route('/', methods=['GET'])
def home():
    """
    function that renders home.html
    """
    context = {}
    if current_user.is_authenticated:
        response = requests.get(url=f'{request.url_root}api/v1/balances/{current_user.id}')
        if response.status_code == 200:
            context = {'balances': response.json()}
    return render_template('home.html', context=context)


@blueprint.route('/add-balance', methods=['GET', 'POST'])
@login_required
def add_balance():
    form = BalanceForm()

    coins = requests.get(url=f'{request.url_root}api/v1/coins')

    if coins.status_code == 200:
        available_coins = [
            (coin['id'], coin['abbreviation'])
            for coin in coins.json()
        ]
        form.coin.choices = available_coins

    if form.validate_on_submit():
        response = requests.post(
            url=f'{request.url_root}api/v1/balances',
            json={
                'user_id': current_user.id,
                'coin_id': int(form.coin.data),
                'amount': str(form.amount.data)
            }
        )
        if response.status_code == 201:
            flash('Coin Added Successfully!')
            return redirect(url_for('blueprint.home'))
        else:
            flash('Something went wrong, please try again!')
    return render_template('balance.html', form=form)


@blueprint.route('/delete-balance/<int:balance_id>', methods=['GET', 'POST'])
@login_required
def delete_balance(balance_id: int):
    response = requests.delete(url=f'{request.url_root}api/v1/balances/{balance_id}')
    if response.status_code == 204:
        flash("Balance deleted")

    return redirect(url_for('blueprint.home'))


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    """
    function that renders register.html
    """
    form = RegistrationForm()
    email = form.email.data
    if form.validate_on_submit():
        response = requests.post(
            url=f'{request.url_root}api/v1/users',
            json={'email': form.email.data, 'password': form.password.data}
        )
        if response.status_code in [200, 201]:
            flash('User Registered Successfully!')
            login_user(CustomUser.create_from_api(response.headers.get('Location')))
            return redirect(url_for('blueprint.home'))
        else:
            flash('Something went wrong!')
    return render_template('register.html', form=form, email=email)


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    """
    function that renders login.html
    """
    form = LoginForm()
    if form.validate_on_submit():
        response = requests.post(
            url=f'{request.url_root}api/v1/users',
            json={'email': form.email.data, 'password': form.password.data}
        )
        if response.status_code == 200:
            flash('User Logged Successfully!')
            login_user(CustomUser.create_from_api(response.headers.get('Location')))

            return redirect(url_for('blueprint.home'))

        flash('Sorry, Wrong Credentials! Try Again...')
    return render_template('login.html', form=form)


@blueprint.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('You have been logout successfully!')
    return redirect(url_for('blueprint.home'))
