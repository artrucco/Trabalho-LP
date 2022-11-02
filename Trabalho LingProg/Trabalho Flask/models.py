from __main__ import db #deste pacote atual importa o objeto db (main)
from flask_login import UserMixin
from sqlalchemy import func

#notas pertencem a usuarios
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now()) #pega a data e hora atual
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #deve receber um id de um usuario existente (pai)

#modelo de usuario
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    senha = db.Column(db.String(150))
    primeiro_nome = db.Column(db.String(150))
    #relacao de parentesco
    notes = db.relationship('Note')