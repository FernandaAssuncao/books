from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)

app.config['SECRET_KEY'] = '4e53ec6f541e0e15fe810f3dd9296b12770647dab495e22f'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///livro.db'

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Faça Login ou Crie sua Conta para Vizualizar está Pagína!'
login_manager.login_message_category = 'alert-info'

from Site import routes
