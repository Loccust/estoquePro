from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/api/registro', methods=['POST'])
def registro():
    data = request.get_json()
    hashed_password = generate_password_hash(data['senha'], method='sha256')
    
    novo_usuario = Usuario(
        nome=data['nome'],
        email=data['email'],
        senha=hashed_password
    )
    
    db.session.add(novo_usuario)
    db.session.commit()
    
    return jsonify({'mensagem': 'Usuário registrado com sucesso'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    usuario = Usuario.query.filter_by(email=data['email']).first()
    
    if not usuario or not check_password_hash(usuario.senha, data['senha']):
        return jsonify({'mensagem': 'Credenciais inválidas'}), 401
    
    # Gerar  token JWT
    access_token = create_access_token(identity=usuario.id)
    
    return jsonify({
        'access_token': access_token,
        'usuario_id': usuario.id,
        'nome': usuario.nome
    }), 200
