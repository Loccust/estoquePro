from flasgger import Swagger
from flask import Flask, redirect
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api

from src.auth.routes import auth_bp
from src.config import Config
from src.models import db
from src.resources.produto_resource import ListaDeProdutosResource, ProdutoResource
from src.swagger_config import swagger_config, swagger_template

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)
    db.init_app(app)
    jwt = JWTManager(app)  # Corrigido: atribua a uma variável
    api = Api(app)

    Swagger(app, config=swagger_config, template=swagger_template)

    # Registre blueprints e recursos PRIMEIRO
    app.register_blueprint(auth_bp)
    api.add_resource(ListaDeProdutosResource, '/produtos')
    api.add_resource(ProdutoResource, '/produtos/<int:id>')  # Rota corrigida

    # DEPOIS crie o banco de dados
    with app.app_context():
        db.create_all()

    @app.route('/')
    def redirect_to_docs():
        return redirect('/apidocs')

    return app
