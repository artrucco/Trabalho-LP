from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user

from models import Note
from __main__ import db
import json

views = Blueprint(__name__,"views")

@views.route("/", methods=['GET','POST'])
@login_required
def home():
    #adicionar ou remover anotações
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) < 1:
            flash('Anotação invalida.', category = 'error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Anotação adicionada', category = 'success')

    return render_template("index.html", user = current_user)

@views.route("/profile")
def profile():
    return render_template("profile.html")

@views.route("/go-to-home")
@login_required
def go_to_home():
    return render_template('index.html')

@views.route("/sign-up")
def to_sign_up():
    return render_template('sign_up.html')

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
