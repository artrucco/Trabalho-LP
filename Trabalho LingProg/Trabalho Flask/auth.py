from unicodedata import category
from flask import Blueprint, render_template, request, flash, redirect

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    data = request.form
    print(data)
    return render_template("login.html")

@auth.route('/logout')
def logout():
    return "<p>Logout</p>"

#criar usuario novo
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        primeiroNome = request.form.get('primeiroNome')
        senha1 = request.form.get('senha1')
        senha2 = request.form.get('senha2')

        #checar validade do usuario novo
        if len(email) < 4:
            flash('Email deve ser maior', category='error')
            return redirect('/sign_up.html')
        elif len(primeiroNome) < 2:
            flash('Nome deve conter mais que dois caracteres', category='error')
            return redirect('/sign_up.html')
        elif senha1 != senha2:
            flash('senhas nao sao iguais', category='error')
            return redirect('/sign_up.html')
        elif len(senha1) < 7:
            flash('Senha deve conter ao menos 7 caracteres', category='error')
            return redirect('/sign_up.html')
        else:
            #adiciona usuario novo a databse
            flash('Conta criada com sucesso!', category='success')
            return redirect('/sign_up.html')

    return render_template("sign_up.html")