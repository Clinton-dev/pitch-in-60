from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from pitch import db, bcrypt
from pitch.models import User, Pitch
from pitch.users.forms import (RegistrationForm, LoginForm, UpdateUserForm,
                                   RequestResetForm, ResetPasswordForm)
from pitch.users.utils import save_picture, send_welcome_email

users = Blueprint('users', __name__)

@users.route("/signup", methods=['POST','GET'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_pass, email=form.email.data)
        db.session.add(user)
        db.session.commit()
        query_user = User.query.filter_by(username=form.username.data).first()
        # send_welcome_email(query_user) will fix this later
        flash(f'A welcome email was sent to your email account you can proceed to login','success')
        return redirect(url_for('login'))

    return render_template("signup.html", title="Signup", form=form)

@users.route("/login", methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash(f'Login unsuccessful check password or email','danger')
    return render_template("login.html", title="Login", form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect('login')

@users.route("/account", methods=['POST','GET'])
@login_required
def account():
    form = UpdateUserForm()
    if form.validate_on_submit():
        if form.image.data:
            picture_file = save_picture(form.image.data)
            current_user.image_file = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account details successfully updated', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    img_file = url_for('static', filename='profile-pics/' + current_user.image_file)

    return render_template("account.html", title="user account", image_file=img_file, form=form)

@users.route("/user/<string:username>")
def user_pitches(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    pitches = Pitch.query.filter_by(author=user)\
        .order_by(Pitch.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template("user_pitches.html", pitches=pitches, user=user)
