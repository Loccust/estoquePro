# src/auth/routes.py
from flasgger import swag_from
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

from src.models.usuario import Usuario 
from src.extensions import db # Mantenha esta importação para acesso direto se necessário

auth_bp = Blueprint('auth_blueprint', __name__, url_prefix='/auth')

@auth_bp.route("/register", methods=["POST"])
@swag_from({
    'tags': ['Autenticação'], 
    'summary': 'Registrar um novo usuário',
    'parameters': [{
        'name': 'body',
        'in': 'body',
        'required': True,
        'schema': {
            'type': 'object',
            'properties': {
                'username': {'type': 'string', 'example': 'novo_usuario'},
                'password': {'type': 'string', 'example': 'senha_secreta123'},
                'name': {'type': 'string', 'example': 'Nome Completo'}
            },
            'required': ['username', 'password', 'name']
        }
    }],
    'responses': {
        201: {
            'description': 'Usuário registrado com sucesso', 
            'schema': {
                'type': 'object',
                'properties': {
                    'msg': {'type': 'string', 'example': 'Usuário registrado com sucesso'}
                }
            }
        },
        400: {
            'description': 'Dados ausentes na requisição', 
            'schema': {
                'type': 'object',
                'properties': {
                    'msg': {'type': 'string', 'example': 'Nome de usuário, senha e nome completo são obrigatórios'}
                }
            }
        },
        409: { 
            'description': 'Usuário já existe',
            'schema': {
                'type': 'object',
                'properties': {
                    'msg': {'type': 'string', 'example': 'Nome de usuário já existe'}
                }
            }
        }
    }
})
def register():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password') or not data.get('name'):
        return jsonify({"msg": "Nome de usuário, senha e nome completo são obrigatórios"}), 400

    username = data['username']
    password = data['password']
    name = data['name']

    # Use find_by_username para verificar se o usuário já existe
    if Usuario.find_by_username(username):
        return jsonify({"msg": "Usuário já existe"}), 409

    # Cria a instância do Usuario
    new_user = Usuario(username=username, password="", name=name)
    new_user.set_password(password) # Hash a senha
    
    # Chama o método .save() que agora fará a inserção no MongoDB
    # usando new_user.to_dict() internamente.
    new_user.save() 

    return jsonify({"msg": "Usuário registrado com sucesso"}), 201


@auth_bp.route("/login", methods=["POST"])
@swag_from({
    'tags': ['Autenticação'], 
    'summary': 'Autenticar usuário e obter token JWT',
    'parameters': [{
        'name': 'body',
        'in': 'body',
        'required': True,
        'schema': {
            'type': 'object',
            'properties': {
                'username': {'type': 'string', 'example': 'testuser'},
                'password': {'type': 'string', 'example': 'password123'}
            },
            'required': ['username', 'password']
        }
    }],
    'responses': {
        200: {
            'description': 'Login bem-sucedido, retorna token JWT', 
            'schema': {
                'type': 'object',
                'properties': {
                    'access_token': {'type': 'string', 'example': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwMDAwMDAwMCwianRpIjoiZmQwYmRkNzgtOWQxMi00YzY4LThkNzYtNzBhMzQxYzg0YjIxIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjY1YmEzY2UxNzU4YTI3ZDdjNDg1YWE5MiIsIm5iZiI6MTcwMDAwMDAwMCwiZXhwIjoxNzAwMDAzNjAwfQ.SignatureHere'}
                }
            }
        },
        400: {
            'description': 'Nome de usuário ou senha ausentes', 
            'schema': {
                'type': 'object',
                'properties': {
                    'msg': {'type': 'string', 'example': 'Nome de usuário ou senha ausentes'}
                }
            }
        },
        401: { 
            'description': 'Credenciais inválidas',
            'schema': {
                'type': 'object',
                'properties': {
                    'msg': {'type': 'string', 'example': 'Nome de usuário ou senha inválidos'}
                }
            }
        }
    }
})
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if not username or not password:
        return jsonify({"msg": "Nome de usuário ou senha ausentes"}), 400

    user = Usuario.find_by_username(username)

    if user and user.check_password(password):
        token = create_access_token(identity=str(user._id), expires_delta=timedelta(hours=1))
        return jsonify(access_token=token), 200
    
    return jsonify({"msg": "Credenciais inválidas"}), 401


# Rota /protected (se você a tiver, com JWT_REQUIRED)
@auth_bp.route('/protected', methods=['GET'])
@swag_from({
    'tags': ['Autenticação'],
    'summary': 'Acessar rota protegida por token JWT',
    'security': [{
        'BearerAuth': [] 
    }],
    'responses': {
        200: {
            'description': 'Acesso concedido',
            'schema': {
                'type': 'object',
                'properties': {
                    'logged_in_as': {'type': 'string', 'example': 'testuser'},
                    'full_name': {'type': 'string', 'example': 'Nome Completo'}
                }
            }
        },
        401: {
            'description': 'Token JWT ausente, inválido ou expirado',
            'schema': {
                'type': 'object',
                'properties': {
                    'msg': {'type': 'string', 'example': 'Signature verification failed'}
                }
            }
        },
        404: {
            'description': 'Usuário não encontrado (identidade do token inválida)',
            'schema': {
                'type': 'object',
                'properties': {
                    'msg': {'type': 'string', 'example': 'Usuário não encontrado'}
                }
            }
        }
    }
})
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    user = Usuario.find_by_id(current_user_id) 
    if user:
        return jsonify(logged_in_as=user.username, full_name=user.name), 200
    return jsonify({"msg": "Usuário não encontrado"}), 404