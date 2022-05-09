from flask import render_template, url_for, flash, redirect, request, abort,Blueprint
from flask_login import current_user, login_required
from pitch import db
from pitch.models import Pitch
from pitch.pitches.forms import PitchForm


pitches = Blueprint('pitches', __name__)

@pitches.route("/pitch/new", methods=['POST','GET'])
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

@pitches.route("/pitch/<int:pitch_id>")
def pitch(pitch_id):
    pitch = Pitch.query.get(pitch_id)
    return render_template("pitch.html", title="New pitch", pitch = pitch)

@pitches.route("/pitch/update/<int:pitch_id>", methods=['POST','GET'])
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

@pitches.route("/pitch/delete/<int:pitch_id>", methods=['POST','GET'])
@login_required
def delete_pitch(pitch_id):
    pitch = Pitch.query.get_or_404(pitch_id)
    if current_user != pitch.author:
        abort(403)
    db.session.delete(pitch)
    db.session.commit()
    flash('Pitch was deleted successfully','success')
    return redirect(url_for('index'))

