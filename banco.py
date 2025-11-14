from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# Configuração do banco de dados
DATABASE = 'conecta_cidadania.db'

def get_db():
    """Conecta ao banco de dados"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Inicializa o banco de dados com a tabela de solicitações"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Criar tabela de solicitações
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS solicitacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            protocolo TEXT UNIQUE NOT NULL,
            nome TEXT NOT NULL,
            matricula TEXT NOT NULL,
            cargo TEXT NOT NULL,
            local TEXT NOT NULL,
            descricao TEXT NOT NULL,
            categoria TEXT NOT NULL,
            status TEXT DEFAULT 'Pendente',
            data_abertura TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Banco de dados inicializado com sucesso!")

# Inicializar banco ao iniciar a aplicação
init_db()

def gerar_protocolo():
    """Gera um número de protocolo único"""
    import random
    while True:
        protocolo = f"{random.randint(100000, 999999)}"
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM solicitacoes WHERE protocolo = ?', (protocolo,))
        if not cursor.fetchone():
            conn.close()
            return protocolo
        conn.close()

# ============ ROTAS DA API ============

@app.route('/')
def home():
    """Serve o arquivo HTML"""
    return send_from_directory('.', 'index.html')

@app.route('/api/solicitacoes', methods=['GET'])
def listar_solicitacoes():
    """Lista todas as solicitações"""
    status = request.args.get('status')
    
    conn = get_db()
    cursor = conn.cursor()
    
    if status:
        cursor.execute('SELECT * FROM solicitacoes WHERE status = ? ORDER BY data_abertura DESC', (status,))
    else:
        cursor.execute('SELECT * FROM solicitacoes ORDER BY data_abertura DESC')
    
    solicitacoes = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify(solicitacoes)

@app.route('/api/solicitacoes', methods=['POST'])
def criar_solicitacao():
    """Cria uma nova solicitação"""
    dados = request.json
    
    # Validação dos campos obrigatórios
    campos_obrigatorios = ['nome', 'matricula', 'cargo', 'local', 'descricao', 'categoria']
    for campo in campos_obrigatorios:
        if not dados.get(campo):
            return jsonify({'erro': f'Campo {campo} é obrigatório'}), 400
    
    try:
        protocolo = gerar_protocolo()
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO solicitacoes 
            (protocolo, nome, matricula, cargo, local, descricao, categoria)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            protocolo,
            dados['nome'],
            dados['matricula'],
            dados['cargo'],
            dados['local'],
            dados['descricao'],
            dados['categoria']
        ))
        conn.commit()
        solicitacao_id = cursor.lastrowid
        
        # Buscar a solicitação criada para retornar
        cursor.execute('SELECT * FROM solicitacoes WHERE id = ?', (solicitacao_id,))
        solicitacao = dict(cursor.fetchone())
        conn.close()
        
        return jsonify({
            'mensagem': 'Solicitação criada com sucesso',
            'protocolo': protocolo,
            'solicitacao': solicitacao
        }), 201
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@app.route('/api/solicitacoes/<int:id>', methods=['GET'])
def buscar_solicitacao(id):
    """Busca uma solicitação específica por ID"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM solicitacoes WHERE id = ?', (id,))
    solicitacao = cursor.fetchone()
    conn.close()
    
    if solicitacao:
        return jsonify(dict(solicitacao))
    return jsonify({'erro': 'Solicitação não encontrada'}), 404

@app.route('/api/solicitacoes/protocolo/<protocolo>', methods=['GET'])
def buscar_por_protocolo(protocolo):
    """Busca uma solicitação pelo número de protocolo"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM solicitacoes WHERE protocolo = ?', (protocolo,))
    solicitacao = cursor.fetchone()
    conn.close()
    
    if solicitacao:
        return jsonify(dict(solicitacao))
    return jsonify({'erro': 'Solicitação não encontrada'}), 404

@app.route('/api/solicitacoes/<int:id>/status', methods=['PUT'])
def atualizar_status(id):
    """Atualiza o status de uma solicitação"""
    dados = request.json
    novo_status = dados.get('status')
    
    if not novo_status:
        return jsonify({'erro': 'Status é obrigatório'}), 400
    
    status_validos = ['Pendente', 'Em Andamento', 'Concluída', 'Cancelada']
    if novo_status not in status_validos:
        return jsonify({'erro': f'Status inválido. Use: {", ".join(status_validos)}'}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE solicitacoes 
        SET status = ?, data_atualizacao = CURRENT_TIMESTAMP 
        WHERE id = ?
    ''', (novo_status, id))
    conn.commit()
    
    if cursor.rowcount == 0:
        conn.close()
        return jsonify({'erro': 'Solicitação não encontrada'}), 404
    
    conn.close()
    return jsonify({'mensagem': 'Status atualizado com sucesso'})

@app.route('/api/solicitacoes/<int:id>', methods=['PUT'])
def atualizar_solicitacao(id):
    """Atualiza uma solicitação completa"""
    dados = request.json
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE solicitacoes 
        SET nome = ?, matricula = ?, cargo = ?, local = ?, 
            descricao = ?, categoria = ?, status = ?,
            data_atualizacao = CURRENT_TIMESTAMP
        WHERE id = ?
    ''', (
        dados.get('nome'),
        dados.get('matricula'),
        dados.get('cargo'),
        dados.get('local'),
        dados.get('descricao'),
        dados.get('categoria'),
        dados.get('status', 'Pendente'),
        id
    ))
    conn.commit()
    
    if cursor.rowcount == 0:
        conn.close()
        return jsonify({'erro': 'Solicitação não encontrada'}), 404
    
    conn.close()
    return jsonify({'mensagem': 'Solicitação atualizada com sucesso'})

@app.route('/api/solicitacoes/<int:id>', methods=['DELETE'])
def deletar_solicitacao(id):
    """Deleta uma solicitação"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM solicitacoes WHERE id = ?', (id,))
    conn.commit()
    
    if cursor.rowcount == 0:
        conn.close()
        return jsonify({'erro': 'Solicitação não encontrada'}), 404
    
    conn.close()
    return jsonify({'mensagem': 'Solicitação deletada com sucesso'})

@app.route('/api/estatisticas', methods=['GET'])
def estatisticas():
    """Retorna estatísticas gerais do sistema"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Total de solicitações
    cursor.execute('SELECT COUNT(*) as total FROM solicitacoes')
    total = cursor.fetchone()['total']
    
    # Solicitações por status
    cursor.execute('SELECT status, COUNT(*) as quantidade FROM solicitacoes GROUP BY status')
    por_status = [dict(row) for row in cursor.fetchall()]
    
    # Solicitações por categoria
    cursor.execute('SELECT categoria, COUNT(*) as quantidade FROM solicitacoes GROUP BY categoria ORDER BY quantidade DESC')
    por_categoria = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    
    return jsonify({
        'total': total,
        'por_status': por_status,
        'por_categoria': por_categoria
    })

if __name__ == '__main__':
    print("=" * 50)
    print("Servidor Conecta Cidadania iniciado!")
    print("=" * 50)
    print("URL: http://127.0.0.1:5000")
    print(" Banco de dados: conecta_cidadania.db")
    print("\n Endpoints disponíveis:")
    print("  GET    /api/solicitacoes - Lista todas")
    print("  POST   /api/solicitacoes - Cria nova")
    print("  GET    /api/solicitacoes/<id> - Busca por ID")
    print("  GET    /api/solicitacoes/protocolo/<protocolo>")
    print("  PUT    /api/solicitacoes/<id> - Atualiza")
    print("  PUT    /api/solicitacoes/<id>/status")
    print("  DELETE /api/solicitacoes/<id> - Deleta")
    print("  GET    /api/estatisticas - Estatísticas")
    print("=" * 50)
    app.run(debug=True, port=5000)