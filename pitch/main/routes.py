from flask import render_template, request, Blueprint
from pitch.models import Pitch

main = Blueprint('main', __name__)

@main.route("/")
def index():
    page = request.args.get('page', 1, type=int)
    pitches = Pitch.query.order_by(Pitch.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template("home.html", pitches=pitches, title="Pitch in a min")