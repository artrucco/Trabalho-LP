from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user

from models import Note
from __main__ import db
import json
import os
import pandas as pd
import matplotlib.pyplot as plt
import plotly
import plotly.express as px


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
def arquivos(): #ler arquivo csv e escolher entre os arquivos upados para plotagem
    dir_path='static/{}'.format(current_user.primeiro_nome)
    lista_arquivos = os.listdir(dir_path) #pega a lista de arquivos contidos na pasta pessoal do usuario
    if request.method == 'POST':
        file = request.form.get('database') #pega a database selecionada no dropdown
        data = pd.read_csv(f"{dir_path}/{file}") #ler a database selecionada no dropdown

        country = 'Brazil'
        year = '2019'

        #grafico 1 - top 10 causas de mortes 
        data_country = data[data['Country/Territory'] == country]
        min_year, max_year = data_country['Year'].min(), data_country['Year'].max()
        fig1 = px.bar(data_country.iloc[:,2:].sum().sort_values(ascending=False).head(10), title='Top 10 Causas de mortes: {} entre {} e {}'.format(country, min_year, max_year), color_discrete_sequence=px.colors.qualitative.Pastel, labels={'value': 'Mortes', 'index': 'Causas de mortes'})
        fig1.update_layout(showlegend=False)
        fig1.show()

        graph1JSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder) #codificação em json para conversar com o html

        cause_of_deaths = ['Meningitis',
       'Alzheimer\'s Disease and Other Dementias', 'Parkinson\'s Disease',
       'Nutritional Deficiencies', 'Malaria', 'Drowning',
       'Interpersonal Violence', 'Maternal Disorders', 'HIV/AIDS',
       'Drug Use Disorders', 'Tuberculosis', 'Cardiovascular Diseases',
       'Lower Respiratory Infections', 'Neonatal Disorders',
       'Alcohol Use Disorders', 'Self-harm', 'Exposure to Forces of Nature',
       'Diarrheal Diseases', 'Environmental Heat and Cold Exposure',
       'Neoplasms', 'Conflict and Terrorism', 'Diabetes Mellitus',
       'Chronic Kidney Disease', 'Poisonings', 'Protein-Energy Malnutrition',
       'Road Injuries', 'Chronic Respiratory Diseases',
       'Cirrhosis and Other Chronic Liver Diseases', 'Digestive Diseases',
       'Fire, Heat, and Hot Substances', 'Acute Hepatitis']

        data['Total_no_of_Deaths'] = data[cause_of_deaths].sum(axis=1)

        Total_no_of_Deaths_data = data[data['Country/Territory']==country].sort_values(by='Total_no_of_Deaths',ascending=False)

        plt.figure(figsize=(8,4),dpi=200)

        #grafico 2 - total de mortes entre os anos 1990 - 2019
        fig2 = px.scatter(Total_no_of_Deaths_data, x='Year', y='Total_no_of_Deaths', title='Número total de mortes entre 1990 e 2019: {}'.format(country),color='Interpersonal Violence', labels={'value': 'Total de mortes', 'index': 'Ano'})
        fig2.show()

        graph2JSON = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
        #graph2JSON = fig2.to_json()

        return render_template('plots.html', user = current_user, graph1JSON = graph1JSON, graph2JSON = graph2JSON)
        
    return render_template('arquivos.html', user=current_user, arquivos = lista_arquivos)

@views.route('arquivos/plot', methods=['POST','GET'])
@login_required
def plot(): #plotagem e visualização dos dados
    return render_template('plots.html', user=current_user)


@views.route('/dash', methods = ['GET','POST'])
def dash(): #escolher uma coluna do csv upado e plotar grafico
    if request.method == 'POST':
        variable = request.form['variable']
        data = pd.read_csv('static/{}/cause_of_deaths.csv'.format(current_user.primeiro_nome))
        plt.scatter(range(len(data[variable])), data[variable])
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
