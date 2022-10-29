from xml.etree.ElementTree import fromstring
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from views import views
from auth import auth

db = SQLAlchemy()
DB_NAME = "database.db"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'HU3HU3HU3'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
db.init_app(app)

app.register_blueprint(views, url_prefix="/")
app.register_blueprint(auth, url_prefix="/")

if __name__ == '__main__':
    app.run(debug=True)