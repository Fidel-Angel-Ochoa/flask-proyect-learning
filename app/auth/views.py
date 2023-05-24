from tabnanny import check
from flask import render_template, redirect, flash, url_for, session, request
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from app.forms import LoginForm
from . import auth

from app.firestore_service import  get_user, user_put
from app.models import UserModel, UserData

@auth.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    context = {
        'login_form':login_form
    }

    form=LoginForm(request.form)
    if request.method == 'POST':
        username= form.username.data
        password = form.password.data

        user_doc = get_user(username)

        if user_doc.to_dict() is not None:

            # password_from_db = user_doc.to_dict()['password'] # esta linea se usaba cuando no hasheabamos los passwords.
            
            if check_password_hash or password(user_doc.to_dict()['password'], password):
                user_data =UserData(username, password)
                user = UserModel(user_data)

                login_user(user)

                flash('Welcome again')

                redirect(url_for('hello'))

            else:
                flash('The information does not match')

        else:
            flash('The username does no exist')

        return redirect(url_for('index'))
        
    return render_template('login.html', **context)

@auth.route('signup', methods=['GET','POST'])
def signup():
    signup_form = LoginForm()
    context = {
        'signup_form': signup_form
    }

    form=LoginForm(request.form)
    if request.method=='POST':
        username= form.username.data
        password = form.password.data

        user_doc = get_user(username)
        if user_doc.to_dict() is None:
            password_hash = generate_password_hash(password)
            user_data = UserData(username, password_hash)
            user_put(user_data)

            user = UserModel(user_data)

            login_user(user)

            flash('Welcome buddy')

            return redirect(url_for('hello'))
        
        else:
            flash('The user already exist')

    return render_template('signup.html', **context)


@auth.route('logout')
@login_required
def logout():
    logout_user()
    flash('Comeback soon')

    return redirect(url_for('auth.login'))
    