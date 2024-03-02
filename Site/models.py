from Site import database, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))


class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    foto_perfil = database.Column(database.String, default='padrao.png')
    favoritos = database.Column(database.String, nullable=False, default='não informado')


class Livro(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String, nullable=False)
    sobre = database.Column(database.Text, nullable=False)
    categoria = database.Column(database.String, nullable=False)
    foto_capa = database.Column(database.String, nullable=False)
