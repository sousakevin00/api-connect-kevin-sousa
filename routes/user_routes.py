from flask import Blueprint, request, jsonify
# Importamos as funções de persistência e geração de ID que criamos no db_manager
from data.db_manager import ler_registos, salvar_registos, gerar_id_unico

# Criação do Blueprint para modularizar as rotas de usuários
user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/usuarios', methods=['GET'])
def listar_usuarios():
    """
    Rota GET: Recupera e retorna a lista completa de usuários.
    Status Code esperado em caso de sucesso: 200 (OK).
    """
    usuarios = ler_registos()
    return jsonify(usuarios), 200

@user_bp.route('/usuarios', methods=['POST'])
def criar_usuario():
    """
    Rota POST atualizada com validação de entrada e respostas padronizadas.
    Assegura que 'nome' e 'email' sejam fornecidos e retorna no formato {"data": ...} ou {"error": ...}.
    """
    dados_recebidos = request.get_json()
    
    # Validação de Entrada: Verifica se o JSON foi enviado
    if not dados_recebidos:
        return jsonify({"error": "Corpo da requisição ausente ou formato inválido."}), 400

    # Validação de Entrada: Verifica os campos obrigatórios
    if 'nome' not in dados_recebidos or not str(dados_recebidos['nome']).strip():
        return jsonify({"error": "O campo 'nome' é obrigatório e não pode estar vazio."}), 400
        
    if 'email' not in dados_recebidos or not str(dados_recebidos['email']).strip():
        return jsonify({"error": "O campo 'email' é obrigatório e não pode estar vazio."}), 400

    # Se passar pela validação, monta o objeto do novo usuário
    novo_usuario = {
        "id": gerar_id_unico(),
        "nome": dados_recebidos["nome"],
        "email": dados_recebidos["email"]
    }

    # Adiciona na persistência
    usuarios = ler_registos()
    usuarios.append(novo_usuario)
    salvar_registos(usuarios)

    # Resposta padronizada de Sucesso usando a chave "data"
    return jsonify({"data": novo_usuario}), 201
@user_bp.route('/usuarios/<id>', methods=['GET'])
def obter_usuario(id):
    """
    Rota GET parametrizada: Busca um usuário específico pelo ID fornecido na URL.
    Trata explicitamente o cenário de ausência, retornando o código 404.
    """
    # Carrega a lista atual de usuários
    usuarios = ler_registos()
    
    # Itera sobre a lista para localizar o usuário com o ID correspondente
    for usuario in usuarios:
        if usuario.get('id') == id:
            # Usuário encontrado: retorna o objeto JSON e o status 200 (OK)
            return jsonify(usuario), 200
            
    # Se o loop terminar e não encontrar ninguém, cai no erro 404 (Not Found)
    return jsonify({"erro": "Usuário não encontrado na base de dados."}), 404
@user_bp.route('/usuarios/<id>', methods=['PUT'])
def atualizar_usuario(id):
    """
    Rota PUT: Localiza um usuário pelo ID e atualiza seus dados.
    Retorna status 200 (OK) em caso de sucesso ou 404 se não existir.
    """
    dados_recebidos = request.get_json()
    usuarios = ler_registos()

    # O enumerate nos dá o índice (i) e o objeto (usuario) ao mesmo tempo
    for i, usuario in enumerate(usuarios):
        if usuario.get('id') == id:
            # Atualiza os campos. O .get() com dois parâmetros mantém o valor antigo 
            # caso o front-end não tenha enviado aquele campo específico na requisição.
            usuarios[i]['nome'] = dados_recebidos.get('nome', usuario.get('nome'))
            usuarios[i]['email'] = dados_recebidos.get('email', usuario.get('email'))
            
            salvar_registos(usuarios)
            return jsonify(usuarios[i]), 200
            
    # Tratamento obrigatório para ID inexistente
    return jsonify({"erro": "Usuário não encontrado para atualização."}), 404

@user_bp.route('/usuarios/<id>', methods=['DELETE'])
def deletar_usuario(id):
    """
    Rota DELETE: Remove um usuário da estrutura de persistência pelo ID.
    Retorna status 200 (OK) com mensagem de sucesso ou 404 se não existir.
    """
    usuarios = ler_registos()

    for i, usuario in enumerate(usuarios):
        if usuario.get('id') == id:
            # Remove o item da lista usando o índice e salva a lista atualizada
            del usuarios[i]
            salvar_registos(usuarios)
            
            # Optamos pelo 200 OK com mensagem de texto (conforme sugerido no enunciado) 
            # para facilitar a visualização do sucesso nos testes do MVP.
            return jsonify({"mensagem": "Usuário removido com sucesso."}), 200

    # Tratamento obrigatório para ID inexistente
    return jsonify({"erro": "Usuário não encontrado para exclusão."}), 404
