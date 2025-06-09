from flasgger import swag_from
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token

from src.models import Usuario, db

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route("/register", methods=["POST"])
@swag_from({
    'tags': ['Auth'],
    'parameters': [{
        'name': 'body',
        'in': 'body',
        'required': True,
        'schema': {
            'type': 'object',
            'properties': {
                'username': {
                    'type': 'string'
                },
                'password': {
                    'type': 'string'
                }
            },
            'required': ['username', 'password']
        }
    }],
    'responses': {
        201: {
            'description': 'Usuário registrado'
        },
        400: {
            'description': 'Usuário já existe'
        }
    }
})
def register():
    data = request.get_json()
    if Usuario.query.filter_by(username=data['username']).first():
        return jsonify({"error": "Usuário já existe"}), 409

    user = Usuario(username=data['username'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "Usuário criado com sucesso."}), 201


@auth_bp.route("/login", methods=["POST"])
@swag_from({
    'tags': ['Auth'],
    'parameters': [{
        'name': 'body',
        'in': 'body',
        'required': True,
        'schema': {
            'type': 'object',
            'properties': {
                'username': {
                    'type': 'string'
                },
                'password': {
                    'type': 'string'
                }
            },
            'required': ['username', 'password']
        }
    }],
    'responses': {
        200: {
            'description': 'Login bem-sucedido'
        },
        401: {
            'description': 'Credenciais inválidas'
        }
    }
})
def login():
    data = request.get_json()
    user = Usuario.query.filter_by(username=data['username']).first()

    if user and user.check_password(data['password']):
        token = create_access_token(identity=str(user.id))
        return jsonify(access_token=token), 200
    return jsonify({"error": "Credenciais inválidas"}), 404