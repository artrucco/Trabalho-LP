from msilib import Table
from xml.etree.ElementTree import fromstring
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def criar_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'HU3HU3HU3'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from views import views
    from auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from models import User, Note

    #cria database de usuarios
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login' #aonde ir caso nao esteja logado
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

app = criar_app()


if __name__ == '__main__':
    app.run(debug=True)