import calculadora
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    etapas=calculadora.calcular();
    return render_template("index.html",etapas=etapas)


if __name__ == "__main__":
    app.run(debug=True);