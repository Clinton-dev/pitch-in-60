from flask import Flask, render_template, url_for
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY']='df84a75c801a375f226ab9fd83b82a'

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

@app.route("/signup")
def signup():
    form = LoginForm()
    return render_template("signup.html", title="Signup", form=form)

@app.route("/login")
def login():
    form = LoginForm()
    return render_template("login.html", title="Signup", form=form)



if __name__ == "__main__":
    app.run(debug=True)