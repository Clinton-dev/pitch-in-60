from flask import Blueprint

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