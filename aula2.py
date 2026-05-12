from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
   return '''
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Currículo</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    margin: 20px;
                    background-color: #f9f9f9;
                    color: #333;
                }
                h1, h2 {
                    color: #2c3e50;
                    text-align: center;
                }
                ul {
                    list-style-type: none;
                    padding: 0;
                    max-width: 600px;
                    margin: 0 auto;
                    background-color: #ffffff;
                    border: 1px solid #ddd;
                    border-radius: 8px;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                    padding: 20px;
                }
                li {
                    margin-bottom: 10px;
                    padding: 8px 0;
                    border-bottom: 1px solid #eee;
                }
                li:last-child {
                    border-bottom: none;
                }
                strong {
                    color: #34495e;
                }
                body {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    min-height: 100vh;
                }
                footer {
                    margin-top: 20px;
                    text-align: center;
                    font-size: 0.9em;
                    color: #666;
                }
            </style>
        </head>
        <body>
            <h1>Currículo</h1>

            <h2>Informações Pessoais</h2>
            <ul>
                <li><strong>Nome:</strong> Felipe Cornélio</li>
                <li><strong>Nascimento:</strong> 10/07/2008</li>
                <li><strong>Idade:</strong> 17</li>
            </ul>

            <h2>Formação</h2>
            <ul>
                <li><strong>Colégio:</strong> Cotemig</li>
                <li><strong>Certificado:</strong> Code Club</li>
            </ul>

            <footer>
                &copy; 2023 - Todos os direitos reservados.
            </footer>
        </body>
        </html>
    '''
if __name__ == '__main__':
    app.run(debug=True)