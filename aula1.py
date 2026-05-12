from flask import Flask

app = Flask(__name__)


@app.route("/decorator")
def decorator():
    return """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Decorators em Python</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                line-height: 1.6;
                margin: 20px;
            }
            h1, h2 {
                color: #2c3e50;
            }
            p {
                margin-bottom: 10px;
            }
            code {
                background-color: #f4f4f4;
                padding: 2px 4px;
                border-radius: 4px;
                font-family: "Courier New", Courier, monospace;
            }
        </style>
    </head>
    <body>
        <h1>O que é um Decorator em Python?</h1>
        <p>Um <strong>decorator</strong> em Python é uma função especial que pode ser usada para modificar ou estender o comportamento de outras funções ou métodos. Ele é aplicado utilizando o símbolo <code>@</code> antes do nome da função decoradora.</p>

        <h2>Para que ele serve?</h2>
        <p>Decorators são usados para reutilizar código, adicionar funcionalidades ou realizar ações antes ou depois da execução de uma função. Eles são muito úteis para tarefas como:</p>
        <ul>
            <li>Autenticação</li>
            <li>Logging</li>
            <li>Controle de acesso</li>
            <li>Validação de dados</li>
        </ul>

        <h2>Como ele é utilizado no Flask?</h2>
        <p>No Flask, decorators são usados para definir rotas e associá-las a funções. Por exemplo:</p>
        <pre><code>@app.route('/home')
    def home():
        return "Bem-vindo à página inicial!"
        </code></pre>
        <p>No exemplo acima, o decorator <code>@app.route</code> associa a URL <code>/home</code> à função <code>home</code>, que retorna o conteúdo exibido no navegador.</p>
    </body>
    </html>
    """
if __name__ == '__main__':
    app.run(debug=True)