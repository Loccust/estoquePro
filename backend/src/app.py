from flask import Flask, redirect
from flask_cors import CORS
from flask_restful import Api
from flasgger import Swagger

from src.config import Config
from src.extensions import jwt
from src.auth.routes import auth_bp
from src.resources.produto_resource import ListaDeProdutosResource, ProdutoResource
from src.swagger_config import swagger_config, swagger_template

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)
    jwt.init_app(app)
    api = Api(app)
    Swagger(app, config=swagger_config, template=swagger_template)

    app.register_blueprint(auth_bp)
    api.add_resource(ListaDeProdutosResource, '/produtos')
    api.add_resource(ProdutoResource, '/produtos/<int:id>') 

    @app.route('/')
    def redirect_to_docs():
        return redirect('/apidocs')

    return app
