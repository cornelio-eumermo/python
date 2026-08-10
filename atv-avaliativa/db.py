import os
import sqlite3

CAMINHO_BANCO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "painel.db")

STATUS_VALIDOS = ("pendente", "em andamento", "concluida")


def conectar():
    conexao = sqlite3.connect(CAMINHO_BANCO)
    conexao.row_factory = sqlite3.Row
    return conexao


def inicializar_banco():
    conexao = conectar()
    conexao.execute(
        """
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL
        )
        """
    )
    conexao.execute(
        """
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descricao TEXT,
            status TEXT NOT NULL DEFAULT 'pendente',
            usuario_id INTEGER NOT NULL,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
        )
        """
    )
    conexao.commit()
    conexao.close()


def executar(sql, parametros=()):
    conexao = conectar()
    cursor = conexao.execute(sql, parametros)
    conexao.commit()
    id_gerado = cursor.lastrowid
    conexao.close()
    return id_gerado


def consultar_um(sql, parametros=()):
    conexao = conectar()
    linha = conexao.execute(sql, parametros).fetchone()
    conexao.close()
    return linha


def consultar_todos(sql, parametros=()):
    conexao = conectar()
    linhas = conexao.execute(sql, parametros).fetchall()
    conexao.close()
    return linhas


def buscar_usuario_por_email(email):
    return consultar_um("SELECT * FROM usuarios WHERE email = ?", (email,))


def criar_usuario(nome, email, senha_hash):
    return executar(
        "INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)",
        (nome, email, senha_hash),
    )


def listar_tarefas(usuario_id, status=None):
    if status and status in STATUS_VALIDOS:
        return consultar_todos(
            "SELECT * FROM tarefas WHERE usuario_id = ? AND status = ? ORDER BY id DESC",
            (usuario_id, status),
        )
    return consultar_todos(
        "SELECT * FROM tarefas WHERE usuario_id = ? ORDER BY id DESC", (usuario_id,)
    )


def buscar_tarefa(tarefa_id, usuario_id):
    return consultar_um(
        "SELECT * FROM tarefas WHERE id = ? AND usuario_id = ?", (tarefa_id, usuario_id)
    )


def criar_tarefa(titulo, descricao, status, usuario_id):
    return executar(
        "INSERT INTO tarefas (titulo, descricao, status, usuario_id) VALUES (?, ?, ?, ?)",
        (titulo, descricao, status, usuario_id),
    )


def atualizar_tarefa(tarefa_id, titulo, descricao, status, usuario_id):
    executar(
        "UPDATE tarefas SET titulo = ?, descricao = ?, status = ? WHERE id = ? AND usuario_id = ?",
        (titulo, descricao, status, tarefa_id, usuario_id),
    )


def excluir_tarefa(tarefa_id, usuario_id):
    executar("DELETE FROM tarefas WHERE id = ? AND usuario_id = ?", (tarefa_id, usuario_id))


def contar_tarefas_por_status(usuario_id):
    linhas = consultar_todos(
        "SELECT status, COUNT(*) as total FROM tarefas WHERE usuario_id = ? GROUP BY status",
        (usuario_id,),
    )
    contagem = {status: 0 for status in STATUS_VALIDOS}
    for linha in linhas:
        contagem[linha["status"]] = linha["total"]
    return contagem
