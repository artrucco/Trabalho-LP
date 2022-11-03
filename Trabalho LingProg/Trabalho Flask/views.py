from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user

from models import Note
from __main__ import db
import json
import os
import pandas as pd
import matplotlib.pyplot as plt

views = Blueprint(__name__,"views")

@views.route("/", methods=['GET','POST'])
@login_required
def home():
    #adicionar nova anotação à pagina inicial do usuario
    if request.method == 'POST':
        note = request.form.get('note')
        if note:
            if len(note) < 1:
                flash('Anotação invalida.', category = 'error')
            else:
                new_note = Note(data=note, user_id=current_user.id)
                db.session.add(new_note)
                db.session.commit()
                flash('Anotação adicionada.', category = 'success')

    return render_template("index.html", user = current_user)

#uploadar um arquivo excel csv que sera copiado e salvo na pasta statics/nome do usuario
@views.route("/upload", methods=['POST', 'GET'])
@login_required
def upload():
    if request.method == 'POST':
        file = request.files['csvfile']
        #se o diretorio static/ nao existe, criar:
        if not os.path.isdir('static/{}'.format(current_user.primeiro_nome)):
            os.mkdir('static/{}'.format(current_user.primeiro_nome))
        filepath = os.path.join('static/{}'.format(current_user.primeiro_nome), file.filename)
        file.save(filepath) #salva o arquivo escolhido no path static 

        data = pd.read_csv('static/{}/{}'.format(current_user.primeiro_nome, file.filename))
        flash('O nome do arquivo enviado é: {}'.format(file.filename), category='success')
        #return render_template('arquivos.html', user = current_user, data=data.to_html())
                 
    return render_template("upload.html", user = current_user)

@views.route('/arquivos', methods=['POST','GET'])
@login_required
def arquivos(): #ler arquivo csv e realizar os plots
    dir_path='static/{}'.format(current_user.primeiro_nome)
    lista_arquivos = os.listdir(dir_path) #pega a lista de arquivos contidos na pasta pessoal do usuario
    if request.method == 'POST':
        file = request.form.get('database') #pega a database selecionada no dropdown
        data = pd.read_csv(f"{dir_path}/{file}") #ler a database selecionada no dropdown

        return render_template('plots.html', user = current_user, data=data.to_html())
    return render_template('arquivos.html', user=current_user, arquivos = lista_arquivos)

#@views.route('arquivos/plot', methods=['POST','GET'])
#@login_required
#def plot():


@views.route('/dash', methods = ['GET','POST'])
def dash(): #escolher uma coluna do csv upado e plotar grafico
    if request.method == 'POST':
        variable = request.form['variable']
        data = pd.read_csv('static/exemplo.csv')
        plt.bar(range(len(data[variable])), data[variable])
        imagepath = os.path.join('static', 'image' + '.png')
        plt.savefig(imagepath)
        return render_template('image.html', image = imagepath)
    return render_template('dash.html')

#retorna ao template inicial
@views.route("/go-to-home")
@login_required
def go_to_home():
    return render_template('index.html')

@views.route("/sign-up")
def to_sign_up():
    return render_template('sign_up.html')

#deleta anotação
@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            flash('Anotação removida: {}'.format(note.data), category='success')

    return jsonify({})
