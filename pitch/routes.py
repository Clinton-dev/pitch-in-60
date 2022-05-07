from flask import render_template, url_for, flash, redirect
from pitch import app
from pitch.forms import RegistrationForm, LoginForm
from pitch.models import User, Pitch

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
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account has been created for {form.username.data}!','success')
        return redirect(url_for('index'))

    return render_template("signup.html", title="Signup", form=form)

@app.route("/login", methods=['POST','GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'clinton@gmail.com' and form.password.data == 'pass':
            flash(f'You have been logged in!','success')
            return redirect(url_for('index'))
        else:
            flash(f'Login unsuccessful check password or email','danger')
    return render_template("login.html", title="Signup", form=form)