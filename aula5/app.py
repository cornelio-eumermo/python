from flask import Flask, render_template_string, request

app = Flask(__name__);

users = {
    "felipe": "22401962",
    "dolga": "cotemig2026",
    "janaina": "cotemig2026",
    "antonio": "cotemig2026",
};


def show_the_login_form():
    return render_template_string("""
        <h2>Login</h2>
        <form method="POST">
            <input type="text" name="usuario" placeholder="Usuário"><br><br>
            <input type="password" name="senha" placeholder="Senha"><br><br>
            <button type="submit">Entrar</button>
        </form>
    """);

def do_the_login():
    in_nome = request.form.get('usuario');
    in_senha = request.form.get('senha');
    if in_nome in users.keys() and in_senha in users.values():
        return f"<h1>Bem-vindo, {in_nome}!</h1>"
    else:
        return "<h1>Login inválido</h1>"


@app.route("/", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return do_the_login();
    else:
        return show_the_login_form();

if __name__ == "__main__":
    app.run(debug=True);