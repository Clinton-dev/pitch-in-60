from flask import render_template, url_for, flash, redirect, request, abort
from pitch import app, db, bcrypt
from pitch.forms import RegistrationForm, LoginForm, UpdateUserForm
from pitch.models import User, Pitch
from flask_login import login_user, current_user, logout_user, login_required

pitches = [
    {
        "user":"Clinton dev",
        "description":"Its not you its me",
        "time_created":"09:30 am"
    },
    {
        "user":"Clinton dev",
        "description":"If you are going through hell keep moving",
        "time_created":"09:50 am"
    }
]

@app.route("/")
def index():
    title ="Pitch in a min"
    return render_template("home.html", pitches=pitches, title=title)

@app.route("/signup", methods=['POST','GET'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_pass, email=form.email.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account is ready you can proceed to login','success')
        return redirect(url_for('login'))

    return render_template("signup.html", title="Signup", form=form)

@app.route("/login", methods=['POST','GET'])
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

@app.route("/logout")
def logout():
    logout_user()
    return redirect('login')

@app.route("/account", methods=['POST','GET'])
@login_required
def account():
    form = UpdateUserForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account details successfully updated', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    # img_file = {{url_for('static',filename='profile-pics/'+ current_user.image_file)}}
    img_file = url_for('static', filename='profile-pics/' + current_user.image_file)

    return render_template("account.html", title="user account", image_file=img_file, form=form)