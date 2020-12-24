from flask import Blueprint, request, session, url_for, render_template, redirect, flash
from models.user import User, UserErrors

user_blueprint = Blueprint('users', __name__)


@user_blueprint.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            User.register_user(email, password)
            session['email'] = email
            return redirect(url_for('assets.index'))
        except UserErrors.UserError:
            pass

    return render_template('users/register.html')


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            if User.is_login_valid(email, password):
                session['email'] = email
                return redirect(url_for('assets.index'))
        except UserErrors.UserError:
            flash('Invalid username or password.', 'danger')

    return render_template("users/login.html")


@user_blueprint.route('/logout')
def logout():
    session['email'] = None
    return redirect(url_for('.login_user'))
