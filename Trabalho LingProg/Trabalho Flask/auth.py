from distutils.log import error
from unicodedata import category
from xmlrpc.client import boolean
from flask import Blueprint, render_template, request, flash, redirect, url_for
from models import User, db
#para nunca guardar a senha como texto, converter a hash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    #data = request.form
    #print(data)
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

        #procurar se o usuario existe na database
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.senha, senha):
                flash('Logado com sucesso!', category = 'success')
                login_user(user, remember = True)
                return redirect(url_for('views.home'))
            else:
                flash('Senha incorreta.', category = 'error')
        else:
            flash('Usuario não existente.', category = 'error')
    return render_template("login.html", boolean=True)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

#criar usuario novo
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        primeiro_nome = request.form.get('primeiro_nome')
        senha1 = request.form.get('senha1')
        senha2 = request.form.get('senha2')

        #checa se usuario ja existe
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email ja cadastrado.', category = 'error')
            return redirect(url_for('views.to_sign_up'))
        #checar validade do usuario novo
        if len(email) < 4:
            flash('Email deve ser maior', category='error')
            return redirect(url_for('auth.sign_up'))
        elif len(primeiro_nome) < 2:
            flash('Nome deve conter mais que dois caracteres', category='error')
            return redirect(url_for('auth.sign_up'))
        elif senha1 != senha2:
            flash('senhas nao sao iguais', category='error')
            return redirect(url_for('auth.sign_up'))
        elif len(senha1) < 7:
            flash('Senha deve conter ao menos 7 caracteres', category='error')
            return redirect(url_for('auth.sign_up'))
        else:
            #adiciona usuario novo a databse
            new_user = User(email=email, primeiro_nome=primeiro_nome, senha=generate_password_hash(senha1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember = True) 
            flash('Conta criada com sucesso!', category='success')
            #redireciona a funcao home em views - pagina inicial
            return redirect(url_for('views.home'))

    return render_template("sign_up.html")