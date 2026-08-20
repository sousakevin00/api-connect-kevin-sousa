import json
import os
import uuid

# Caminho para o ficheiro de base de dados (simulação de persistência)
CAMINHO_FICHEIRO = 'data/database.json'

def inicializar_base_dados():
    """
    Garante que o diretório e o ficheiro JSON existem.
    Se não existirem na máquina, cria-os automaticamente com uma lista vazia,
    preparando o estado inicial do nosso 'banco de dados'.
    """
    if not os.path.exists('data'):
        os.makedirs('data')
    
    if not os.path.exists(CAMINHO_FICHEIRO):
        with open(CAMINHO_FICHEIRO, 'w', encoding='utf-8') as ficheiro:
            # Inicializa com um array (lista) vazio em formato JSON
            json.dump([], ficheiro)

def gerar_id_unico():
    """
    Técnica de Geração de ID: 
    Optou-se por utilizar UUID (Universally Unique Identifier) na sua versão 4.
    Esta técnica gera uma string alfanumérica única (ex: 'f47ac10b-58cc-4372-a567-0e02b2c3d479').
    Ao contrário de IDs incrementais (1, 2, 3...), o UUID garante que não haverá 
    colisões de chaves primárias, mesmo que o ficheiro JSON seja apagado ou o servidor reiniciado.
    """
    return str(uuid.uuid4())

def ler_registos():
    """Lê e retorna a lista de utilizadores guardada no ficheiro JSON."""
    with open(CAMINHO_FICHEIRO, 'r', encoding='utf-8') as ficheiro:
        return json.load(ficheiro)

def salvar_registos(dados):
    """Sobrescreve o ficheiro JSON com a lista de utilizadores atualizada."""
    with open(CAMINHO_FICHEIRO, 'w', encoding='utf-8') as ficheiro:
        json.dump(dados, ficheiro, indent=4, ensure_ascii=False)

# Executa a inicialização para garantir que o ficheiro existe antes de qualquer rota ser chamada
inicializar_base_dados()