from flasgger import swag_from
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from flask import jsonify  # Importe jsonify para respostas consistentes

from src.models import Usuario


class ProfileResource(Resource):
    @swag_from({
        'tags': ['Usuário'],
        'summary': 'Obter dados do perfil autenticado',
        'security': [{
            'BearerAuth': []
        }],
        'responses': {
            200: {
                'description': 'Perfil do usuário',
                'content': {
                    'application/json': {
                        'example': {
                            "id": 1,               # Campo obrigatório
                            "username": "detetivezin"
                        }
                    }
                }
            },
            401: {'description': 'Token inválido ou expirado'},
            404: {'description': 'Usuário não encontrado'}  # Adicione esta resposta
        }
    })
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = Usuario.query.get(user_id)
        
        if not user:
            return {"message": "Usuário não encontrado"}, 404
        
        return jsonify({  # Use jsonify para garantir o formato correto
            "id": user.id,          # Adicione o campo id
            "username": user.username
        })
