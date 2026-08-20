from flask import Flask, jsonify, request

# Instancia o servidor principal da aplicação
app = Flask(__name__)
from routes.user_routes import user_bp
app.register_blueprint(user_bp)

# Configuração para garantir que o retorno JSON respeite a acentuação padrão (UTF-8)
app.config['JSON_AS_ASCII'] = False

# Rota raiz de teste para garantir que o servidor inicializou corretamente
@app.route('/', methods=['GET'])
def health_check():
    """Endpoint de teste para verificar o status do servidor."""
    # O jsonify atua formatando o dicionário Python para uma resposta HTTP estruturada em JSON
    return jsonify({
        "status": "sucesso",
        "mensagem": "Servidor da API Connect inicializado e operando perfeitamente!"
    }), 200

# Bloco de execução principal
if __name__ == '__main__':
    # Coloca o servidor em modo de escuta na porta 5000.
    # O modo debug=True recarrega o servidor automaticamente a cada salvamento do arquivo.
    app.run(host='0.0.0.0', port=5000, debug=True)