from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required, logout_user, current_user, login_user

from .. import app, db
from ..models import User
from ..forms.auth import Login_form

@app.route('/login', methods=['GET', 'POST'])
def login():

    # Check to see if a user is already logged in
    if current_user.is_authenticated:
        flash(f"You are currently logged in as {current_user.username}", category='info')
        return redirect(url_for('home'))

    form = Login_form()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        login_user(user)
        flash('Login Successful', 'info')
        return redirect(url_for('home'))

    return render_template('auth/login.html', title='Login', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout Successful', 'info')
    return redirect(url_for('home'))