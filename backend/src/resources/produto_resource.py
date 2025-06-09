from flask_restful import Resource
from flask import request, jsonify
from src.extensions import db

class ListaDeProdutosResource(Resource):
    # @jwt_required()
    def get(self):
        """
        Lista todos os produtos
        ---
        tags:
          - Produtos
        responses:
          200:
            description: Uma lista de produtos
            schema:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: string
                  nome:
                    type: string
                  descricao:
                    type: string
                  preco:
                    type: number
                  quantidade:
                    type: integer
        """
        produtos = []
        for doc in db.products.find():
            doc['id'] = str(doc['_id'])
            del doc['_id']
            produtos.append(doc)
        return jsonify(produtos)

    # @jwt_required()
    def post(self):
        """
        Cria um novo produto
        ---
        tags:
          - Produtos
        parameters:
          - name: body
            in: body
            required: true
            schema:
              type: object
              properties:
                nome:
                  type: string
                descricao:
                  type: string
                preco:
                  type: number
                quantidade:
                  type: integer
        responses:
          201:
            description: Produto criado com sucesso
            schema:
              type: object
              properties:
                id:
                  type: string
                nome:
                  type: string
        """
        data = request.get_json()
        if not data or not data.get('nome'):
            return {"message": "Nome do produto é obrigatório"}, 400
            
        result = db.products.insert_one(data)
        
        new_product_id = str(result.inserted_id)
        
        return {"message": "Produto criado com sucesso", "id": new_product_id}, 201

class ProdutoResource(Resource):
    # @jwt_required()
    def get(self, id):
        """
        Obtém um produto pelo ID
        ---
        tags:
          - Produtos
        parameters:
          - name: id
            in: path
            type: string
            required: true
        responses:
          200:
            description: Dados do produto
          404:
            description: Produto não encontrado
        """
        try:
            produto = db.products.find_one({"_id": ObjectId(id)})
            if produto:
                produto['id'] = str(produto['_id'])
                del produto['_id']
                return jsonify(produto)
            return {"message": "Produto não encontrado"}, 404
        except Exception: 
            return {"message": "ID de produto inválido"}, 400

    # @jwt_required()
    def put(self, id):
        """
        Atualiza um produto
        ---
        tags:
          - Produtos
        parameters:
          - name: id
            in: path
            type: string
            required: true
          - name: body
            in: body
            required: true
            schema:
              type: object
              properties:
                nome:
                  type: string
                descricao:
                  type: string
                preco:
                  type: number
                quantidade:
                  type: integer
        responses:
          200:
            description: Produto atualizado com sucesso
          404:
            description: Produto não encontrado
        """
        data = request.get_json()
        if not data:
            return {"message": "Nenhum dado fornecido para atualização"}, 400

        try:
            result = db.products.update_one(
                {"_id": ObjectId(id)},
                {"$set": data} 
            )
            if result.matched_count == 0:
                return {"message": "Produto não encontrado"}, 404
            return {"message": "Produto atualizado com sucesso"}, 200
        except Exception:
            return {"message": "ID de produto inválido"}, 400

    # @jwt_required() # Descomente se a rota exigir autenticação
    def delete(self, id):
        """
        Deleta um produto
        ---
        tags:
          - Produtos
        parameters:
          - name: id
            in: path
            type: string
            required: true
        responses:
          200:
            description: Produto deletado com sucesso
          404:
            description: Produto não encontrado
        """
        try:
            result = db.products.delete_one({"_id": ObjectId(id)})
            if result.deleted_count == 0:
                return {"message": "Produto não encontrado"}, 404
            return {"message": "Produto deletado com sucesso"}, 200
        except Exception:
            return {"message": "ID de produto inválido"}, 400