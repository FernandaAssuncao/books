from flask import render_template, url_for, flash, request, redirect
from Site.forms import FormCriarConta, FormLogin, FormEditarPerfil
from Site import app, database, bcrypt
from Site.models import Usuario, Livro
from flask_login import login_user, logout_user, current_user, login_required
from PIL import Image
import secrets
import os


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/livros')
@login_required
def livros():
    livross = Livro.query.all()
    return render_template('livros.html', livros=livross)


@app.route('/livros/<id_livro>')
@login_required
def mostrar_livro(id_livro):
    livro = Livro.query.get(id_livro)
    return render_template('mostrarlivro.html', livro=livro)


@app.route('/usuarios')
@login_required
def usuarios():
    usuarioss = Usuario.query.all()
    return render_template('usuarios.html', usuarioss=usuarioss)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    form_criarconta = FormCriarConta()
    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar_dados.data)
            flash(f'Bem vindo(a) {form_login.email.data}', 'alert-success')
            par_next = request.args.get('next')
            if par_next:
                return redirect(par_next)
            else:
                return redirect(url_for('home'))
        else:
            flash('Falha no login, E-mail ou Senha Incorretos!', 'alert-danger')
    if form_criarconta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        senha_cript = bcrypt.generate_password_hash(form_criarconta.senha.data)
        usuario = Usuario(username=form_criarconta.username.data, email=form_criarconta.email.data,
                          senha=senha_cript)
        database.session.add(usuario)
        database.session.commit()
        flash(f'Conta criada com sucesso no email {form_criarconta.email.data}', 'alert-success')
        return redirect(url_for('home'))
    return render_template('login.html', form_login=form_login, form_criarconta=form_criarconta)


@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash('Logout feito com Sucesso!', 'alert-success')
    return redirect(url_for('home'))


@app.route('/favoritos')
@login_required
def favoritos():
    lista = []
    for livro in current_user.favoritos.split(';'):
        favorito = Livro.query.filter_by(nome=livro).first()
        lista.append(favorito)
    return render_template('favoritos.html', favoritos=lista)


@app.route('/lacamentos')
@login_required
def lacamentos():
    lista = []
    lista = Livro.query.all()
    numero = len(lista)
    lista = [lista[numero - 1], lista[numero - 2], lista[numero - 3], lista[numero - 4]]
    return render_template('lacamentos.html', livros=lista)


@app.route('/meuperfil')
@login_required
def perfil():
    foto_perfil = url_for('static', filename=f'fotos_perfil/{current_user.foto_perfil}')
    return render_template('perfil.html', foto_perfil=foto_perfil)


def salvar_imagem(imagem):
    codigo = secrets.token_hex(8)
    nome, extencao = os.path.splitext(imagem.filename)
    nome_completo = nome + codigo + extencao
    caminho_completo = os.path.join(app.root_path, 'static/fotos_perfil/', nome_completo)
    tamanho = (400, 400)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    imagem_reduzida.save(caminho_completo)
    return nome_completo


@app.route('/meuperfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    foto_perfil = url_for('static', filename=f'fotos_perfil/{current_user.foto_perfil}')
    form = FormEditarPerfil()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.username = form.username.data
        if form.foto_perfil.data:
            nome_imagem = salvar_imagem(form.foto_perfil.data)
            current_user.foto_perfil = nome_imagem
        database.session.commit()
        flash('Perfil atualizado com sucesso!', 'alert-success')
        return redirect(url_for('perfil'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.username.data = current_user.username
    return render_template('editarperfil.html', foto_perfil=foto_perfil, form=form)


@app.route('/livros/adicionar/<id_livro>')
@login_required
def adicionar(id_livro):
    livro = Livro.query.get(id_livro)
    liste = []
    if current_user.favoritos != 'não informado':
        for livross in current_user.favoritos.split(';'):
            liste.append(livross)
        liste.append(livro.nome)
        current_user.favoritos = ';'.join(liste)
        database.session.commit()
    else:
        lista = [livro.nome]
        current_user.favoritos = ';'.join(lista)
        database.session.commit()
    flash('Livro Adicionado com sucesso!', 'alert-success')
    return redirect(url_for('favoritos'))


@app.route('/livros/remover/<id_livro>')
@login_required
def remover(id_livro):
    livro = Livro.query.get(id_livro)
    lista = []
    for livross in current_user.favoritos.split(';'):
        if livross == livro.nome:
            pass
        else:
            lista.append(livross)
        current_user.favoritos = ';'.join(lista)
        database.session.commit()
        if current_user.favoritos == '':
            current_user.favoritos = 'não informado'
            database.session.commit()
    return redirect(url_for('favoritos'))
