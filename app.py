from os import environ
# from datetime import datetime

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

DB_USERNAME = environ.get('DB_USERNAME', 'username')
DB_PASSWORD = environ.get('DB_PASSWORD', 'password')

# adding database
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{DB_USERNAME}:{DB_PASSWORD}@localhost/users'

# initialising database
db = SQLAlchemy(app)


@app.route('/')
def home():
    """
    function that renders home.html
    """
    return render_template('home.html')


@app.route('/register')
def register():
    """
    function that renders register.html
    """
    return render_template('register.html')


@app.route('/login')
def login():
    """
    function that renders login.html
    """
    return render_template('login.html')


if __name__ == '__main__':
    app.run()
