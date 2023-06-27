from flask import Blueprint, render_template, url_for, request, redirect
#from werkzeug.security import generate_password_hash, check_password_hash
from passlib.hash import sha256_crypt
from flask_login import login_user, logout_user, login_required
from .models import User
from . import db

auth = Blueprint('auth', __name__)


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    name = request.form.get('user_name')
    email = request.form.get('user_email')
    password = request.form.get('user_pass')

    # print(name, email, password)
    user = User.query.filter_by(email=email).first()

    if user:
        print('User already exists')
        return redirect(url_for('auth.signup'))

    new_user = User(email=email, name=name,
                    password=sha256_crypt.encrypt(password))
    # # new_user = User(email=email, name=name,
    #                 password=generate_password_hash(password, method='pbkdf2', salt_length=16))
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    print(email, password, remember)
    user = User.query.filter_by(email=email).first()
    hashed_pass = user.password
    # if check_password_hash(hashed_pass, password):
    if sha256_crypt.verify(password, hashed_pass):
        login_user(user, remember=remember)
        return redirect(url_for('main.profile'))
    else:
        return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
