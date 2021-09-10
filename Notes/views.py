from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from Notes.models import note
from Notes import db

views = Blueprint("views", __name__)


@views.route('/', methods=["POST", "GET"])
@login_required
def home():
    if request.method == "POST":
        post = request.form.get('note')
        if len(post) < 1:
            flash("What's the point of making a note if you're not actually going to add anything?!", category="error")
        else:
            new_note = note(data=post, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Note added!", category="Success")
    return render_template('home.html', user=current_user)


@views.route("/delete-note/<int:id>")
def delete_note(id):
    note_to_delete = note.query.get(id)
    db.session.delete(note_to_delete)
    db.session.commit()
    return redirect(url_for("views.home"))
