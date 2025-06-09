@app.route('/api/produtos', methods=['POST'])
@jwt_required()
def criar_produto():
    dados = request.get_json()
    usuario_id = get_jwt_identity()
    
    novo_produto = Produto(
        codigo=dados['codigo'],
        nome=dados['nome'],
        quantidade=dados['quantidade'],
        saida=dados['saida'],
        quantidade_apos_saida=dados['quantidade'] - dados['saida'],
        data=dados['data'],
        setor=dados['setor'],
        usuario_id=usuario_id
    )
    
    db.session.add(novo_produto)
    db.session.commit()
    
    return jsonify({'mensagem': 'Produto criado com sucesso'}), 201

@app.route('/api/produtos', methods=['GET'])
@jwt_required()
def listar_produtos():
    usuario_id = get_jwt_identity()
    produtos = Produto.query.filter_by(usuario_id=usuario_id).all()
    
    return jsonify([{
        'id': p.id,
        'codigo': p.codigo,
        'nome': p.nome,
        'quantidade': p.quantidade,
        'saida': p.saida,
        'quantidade_apos_saida': p.quantidade_apos_saida,
        'data': p.data,
        'setor': p.setor
    } for p in produtos]), 200 
