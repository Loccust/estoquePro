swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Estoque - API de controle de estoque",
        "description": "Uma API para gerenciar produtos em estoque",
        "version": "1.0.0"
    },
    "uiversion": 3,
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Insira o token JWT no formato **Bearer &lt;token&gt;**"
        }
    },
    "security": [{"Bearer": []}],
    "basePath": "/",
    "schemes": ["http"],
    "securityDefinitions": {
        "BearerAuth": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT: Bearer <token>"
        }
    }
}

swagger_config = {
    "headers": [],
    "specs": [{
        "endpoint": 'apispec',
        "route": '/apispec.json',
        "rule_filter": lambda rule: True,  # mostra todas as rotas
        "model_filter": lambda tag: True,
    }],
    "static_url_path":
    "/flasgger_static",
    "swagger_ui":
    True,
    "specs_route":
    "/apidocs/"
}