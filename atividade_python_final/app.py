import os
from functools import wraps

import requests
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

import db

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "chave-de-desenvolvimento-troque-em-producao")
DEBUG = os.environ.get("FLASK_DEBUG", "1") == "1"

URL_API_FRASES = "https://api.adviceslip.com/advice"


def login_obrigatorio(rota):
    @wraps(rota)
    def rota_protegida(*args, **kwargs):
        if "usuario_id" not in session:
            return redirect(url_for("login"))
        return rota(*args, **kwargs)

    return rota_protegida


@app.route("/")
def index():
    if "usuario_id" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")

        if not nome or not email or not senha:
            flash("Preencha nome, e-mail e senha.", "danger")
        elif db.buscar_usuario_por_email(email):
            flash("Já existe uma conta com esse e-mail.", "danger")
        else:
            senha_hash = generate_password_hash(senha)
            db.criar_usuario(nome, email, senha_hash)
            flash("Conta criada com sucesso! Faça login.", "success")
            return redirect(url_for("login"))

    return render_template("registro.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")

        usuario = db.buscar_usuario_por_email(email)
        if usuario and check_password_hash(usuario["senha"], senha):
            session["usuario_id"] = usuario["id"]
            session["usuario_nome"] = usuario["nome"]
            return redirect(url_for("dashboard"))

        flash("E-mail ou senha inválidos.", "danger")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/dashboard")
@login_obrigatorio
def dashboard():
    usuario_id = session["usuario_id"]
    status_filtro = request.args.get("status")
    tarefas = db.listar_tarefas(usuario_id, status_filtro)
    frase_motivacional = buscar_frase_motivacional()

    return render_template(
        "dashboard.html",
        tarefas=tarefas,
        frase=frase_motivacional,
    )


def buscar_frase_motivacional():
    try:
        resposta = requests.get(URL_API_FRASES, timeout=4)
        resposta.raise_for_status()
        return resposta.json()["slip"]["advice"]
    except (requests.RequestException, KeyError, ValueError):
        return "Continue firme com suas tarefas."


@app.route("/api/tarefas")
@login_obrigatorio
def api_listar_tarefas():
    usuario_id = session["usuario_id"]
    status_filtro = request.args.get("status")
    tarefas = db.listar_tarefas(usuario_id, status_filtro)
    return jsonify([dict(tarefa) for tarefa in tarefas])


@app.route("/nova_tarefa", methods=["GET", "POST"])
@login_obrigatorio
def nova_tarefa():
    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        descricao = request.form.get("descricao", "").strip()
        status = request.form.get("status", "pendente")

        if not titulo:
            flash("O título da tarefa é obrigatório.", "danger")
        elif status not in db.STATUS_VALIDOS:
            flash("Status inválido.", "danger")
        else:
            db.criar_tarefa(titulo, descricao, status, session["usuario_id"])
            return redirect(url_for("dashboard"))

    return render_template("form_tarefa.html", tarefa=None, titulo_pagina="Nova tarefa")


@app.route("/editar/<int:tarefa_id>", methods=["GET", "POST"])
@login_obrigatorio
def editar_tarefa(tarefa_id):
    usuario_id = session["usuario_id"]
    tarefa = db.buscar_tarefa(tarefa_id, usuario_id)
    if tarefa is None:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        descricao = request.form.get("descricao", "").strip()
        status = request.form.get("status", "pendente")

        if not titulo:
            flash("O título da tarefa é obrigatório.", "danger")
        elif status not in db.STATUS_VALIDOS:
            flash("Status inválido.", "danger")
        else:
            db.atualizar_tarefa(tarefa_id, titulo, descricao, status, usuario_id)
            return redirect(url_for("dashboard"))

    return render_template("form_tarefa.html", tarefa=tarefa, titulo_pagina="Editar tarefa")


@app.route("/excluir/<int:tarefa_id>", methods=["POST"])
@login_obrigatorio
def excluir_tarefa(tarefa_id):
    db.excluir_tarefa(tarefa_id, session["usuario_id"])
    return redirect(url_for("dashboard"))


@app.route("/dashboard_progresso")
@login_obrigatorio
def dashboard_progresso():
    return render_template("dashboard_progresso.html")


@app.route("/api/progresso")
@login_obrigatorio
def api_progresso():
    contagem = db.contar_tarefas_por_status(session["usuario_id"])
    return jsonify(contagem)


if __name__ == "__main__":
    db.inicializar_banco()
    app.run(debug=DEBUG)
