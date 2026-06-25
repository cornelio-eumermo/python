from flask import Blueprint, redirect, render_template, request, url_for

from models import Filme, Sala, Sessao, db

# Blueprint = módulo de rotas do cinema (registrar no app.py com register_blueprint)
cinema_bp = Blueprint("cinema", __name__, url_prefix="/cinema")


@cinema_bp.route("/")
def index():
    # TODO ALUNO: 
    sessoes = Sessao.listar_com_detalhes()
    return render_template("cinema/lista_sessoes.html", sessoes=sessoes)


@cinema_bp.route("/sessao/cadastrar", methods=["GET", "POST"])
def cadastrar_sessao():
    filmes = Filme.listar()
    salas = Sala.listar()

    if request.method == "POST":
        # TODO ALUNO: criar Sessao com filme_id, sala_id, data_hora, preco
        sessao = Sessao(filme_id=request.form(["filme_id"]), sala_id=request.form(["sala_id"]), data_hora=request.form(["data_hora"]), preco=request.form(["preco"]))
        pass

    return render_template(
        "cinema/formulario_sessao.html",
        filmes=filmes,
        salas=salas,
    )
