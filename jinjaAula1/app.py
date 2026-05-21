from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def questao1():
    return render_template("questao1.html", name="Adão Cornélio")


@app.route("/questao2")
def questao2():
    dados = [
        {"nome": "felipe", "idade": 17},
        {"nome": "felipe", "idade": 17},
        {"nome": "felipe", "idade": 17},
        {"nome": "felipe", "idade": 17},
    ]
    return render_template("questao2.html", alunos=dados)


if __name__ == "__main__":
    app.run(debug=True)
