from flask import Blueprint, redirect, render_template, request, url_for

from models.filme import Filme
from models.sala import Sala
from models.sessao import Sessao
from models.ingresso import Ingresso


dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/")
def index():
    return render_template("index.html", total_filmes=Filme.query.count(),
                           total_salas=Sala.query.count(),
                           total_sessoes=Sessao.query.count(),
                           total_ingressos=Ingresso.query.count())