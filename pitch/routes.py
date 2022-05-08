import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from pitch import app, db, bcrypt
from pitch.forms import RegistrationForm, LoginForm, UpdateUserForm, PitchForm
from pitch.models import User, Pitch
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
def index():
    pitches = Pitch.query.all()
    return render_template("home.html", pitches=pitches, title="Pitch in a min")

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

#
def save_picture(form_picture):
    random_hex =  secrets.token_hex(7)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    pic_file_name = random_hex + f_ext
    pic_path = os.path.join(app.root_path, 'static/profile-pics', pic_file_name)

    output_size = (127, 127)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(pic_path)
    return pic_file_name



@app.route("/account", methods=['POST','GET'])
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
    # img_file = {{url_for('static',filename='profile-pics/'+ current_user.image_file)}}
    img_file = url_for('static', filename='profile-pics/' + current_user.image_file)

    return render_template("account.html", title="user account", image_file=img_file, form=form)

@app.route("/pitch/new", methods=['POST','GET'])
@login_required
def new_pitch():
    form = PitchForm()
    if form.validate_on_submit():
        pitch = Pitch(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(pitch)
        db.session.commit()
        flash("Pitch was successfully created", "success")
        return redirect(url_for('index'))
    return render_template("create_pitch.html", title="New pitch", form = form, legend="Create a pitch")

@app.route("/pitch/<int:pitch_id>")
def pitch(pitch_id):
    pitch = Pitch.query.get(pitch_id)
    return render_template("pitch.html", title="New pitch", pitch = pitch)

@app.route("/pitch/update/<int:pitch_id>", methods=['POST','GET'])
@login_required
def update_pitch(pitch_id):
    pitch = Pitch.query.get_or_404(pitch_id)
    if current_user != pitch.author:
        abort(403)
    form = PitchForm()
    if form.validate_on_submit():
        pitch.title = form.title.data
        pitch.content = form.content.data
        db.session.commit()
        flash('Pitch updated successfully', 'success')
        return redirect(url_for('pitch', pitch_id=pitch.id))
    elif request.method == 'GET':
        form.title.data = pitch.title
        form.content.data = pitch.content
    return render_template("create_pitch.html", title="Update pitch", form = form, legend="Update a pitch")

@app.route("/pitch/delete/<int:pitch_id>", methods=['POST','GET'])
@login_required
def delete_pitch(pitch_id):
    pitch = Pitch.query.get_or_404(pitch_id)
    if current_user != pitch.author:
        abort(403)
    db.session.delete(pitch)
    db.session.commit()
    flash('Pitch was deleted successfully','success')
    return redirect(url_for('index'))