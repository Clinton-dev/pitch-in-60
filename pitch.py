from flask import Flask, render_template

app = Flask(__name__)

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
def hello_world():
    title ="Pitch in a min"
    return render_template("home.html", pitches=pitches, title=title)




if __name__ == "__main__":
    app.run(debug=True)