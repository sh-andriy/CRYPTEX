from os import environ
from datetime import datetime

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

DB_USERNAME = environ.get('DB_USERNAME', 'user')
DB_PASSWORD = environ.get('DB_PASSWORD', 'password')

# adding database
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{DB_USERNAME}:{DB_PASSWORD}@localhost/users'

# initialising database
db = SQLAlchemy(app)




@app.route('/')
def home():
    return render_template('home.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/login')
def login():
    """
    function render login.html
    """
    return render_template('login.html')


if __name__ == '__main__':
    app.run()
