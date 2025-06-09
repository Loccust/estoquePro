from flasgger import swag_from
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource, reqparse
from datetime import date
from src.models import Produto, db 

produto_parser = reqparse.RequestParser()
produto_parser.add_argument('codigo', type=str, required=True, help="O código do produto é obrigatório.")
produto_parser.add_argument('nome', type=str, required=True, help="O nome do produto é obrigatório.")
produto_parser.add_argument('quantidade', type=int, required=True, help="A quantidade é obrigatória.")
produto_parser.add_argument('saida', type=int, default=0, help="A saída do produto (padrão 0).")
produto_parser.add_argument('data', type=str, help="A data do produto (formato YYYY-MM-DD). Padrão é a data atual.")
produto_parser.add_argument('setor', type=str, required=True, help="O setor do produto é obrigatório.")


class ListaDeProdutosResource(Resource):
    @swag_from({
        'tags': ['Produtos'],
        'summary': 'Listar produtos',
        'description': 'Retorna uma lista de todos os produtos.',
        'responses': {
            200: {
                'description': 'Lista de produtos retornada com sucesso',
                'schema': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            'codigo': {'type': 'string', 'example': '24595'},
                            'nome': {'type': 'string', 'example': 'lklkl'},
                            'quantidade': {'type': 'integer', 'example': 50},
                            'saida': {'type': 'integer', 'example': 4},
                            'quantidadeAposSaida': {'type': 'integer', 'example': 46},
                            'data': {'type': 'string', 'format': 'date', 'example': '2025-04-27'},
                            'setor': {'type': 'string', 'example': 'net'},
                        }
                    }
                },
                'examples': {
                    'application/json': [{
                        "codigo": "24595",
                        "nome": "lklkl",
                        "quantidade": 50,
                        "saida": 4,
                        "quantidadeAposSaida": 46,
                        "data": "2025-04-27",
                        "setor": "net"
                    }]
                }
            },
            401: {
                'description': 'Usuário não autenticado'
            },
            500: {
                'description': 'Erro interno do servidor'
            }
        },
        'security': [{'BearerAuth': []}]
    })
    @jwt_required()
    def get(self):
        try:
            produtos = Produto.query.all()
            serialized_produtos = [produto.serialize() for produto in produtos]
            return serialized_produtos, 200
        except Exception as e:
            return {'message': f'Ocorreu um erro ao listar produtos: {str(e)}'}, 500


class ProdutoResource(Resource):
    @swag_from({
        'tags': ['Produtos'],
        'summary': 'Criar um produto',
        'description': 'Cria um novo produto no sistema.',
        'security': [{'BearerAuth': []}],
        'parameters': [{
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'codigo': {'type': 'string', 'example': 'PROD001'},
                    'nome': {'type': 'string', 'example': 'Parafuso M8'},
                    'quantidade': {'type': 'integer', 'example': 500},
                    'saida': {'type': 'integer', 'example': 10},
                    'data': {'type': 'string', 'format': 'date', 'example': '2025-05-26'},
                    'setor': {'type': 'string', 'example': 'Ferragens'}
                },
                'required': ['codigo', 'nome', 'quantidade', 'setor']
            }
        }],
        'responses': {
            201: {
                'description': 'Produto criado com sucesso',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'codigo': {'type': 'integer'},
                        'nome': {'type': 'string'},
                        'quantidade': {'type': 'integer'},
                        'saida': {'type': 'integer'},
                        'quantidadeAposSaida': {'type': 'integer'},
                        'data': {'type': 'string', 'format': 'date'},
                        'setor': {'type': 'string'}
                    }
                }
            },
            400: {'description': 'Dados inválidos ou produto já existente'},
            401: {'description': 'Usuário não autenticado'},
            500: {'description': 'Erro interno do servidor'}
        }
    })
    @jwt_required()
    def post(self):
        try:
            args = produto_parser.parse_args()

            codigo = args['codigo']
            nome = args['nome']
            quantidade = args['quantidade']
            saida = args['saida']
            data_str = args['data']
            setor = args['setor']

            if Produto.query.get(codigo):
                return {'message': f'Produto com código {codigo} já existe.'}, 400

            if quantidade < saida:
                return {'message': 'A quantidade de saída não pode ser maior que a quantidade inicial.'}, 400
            quantidade_apos_saida = quantidade - saida

            data_obj = None
            if data_str:
                try:
                    data_obj = date.fromisoformat(data_str)
                except ValueError:
                    return {'message': 'Formato de data inválido. Use YYYY-MM-DD.'}, 400
            else:
                data_obj = date.today()

            novo_produto = Produto(
                codigo=codigo,
                nome=nome,
                quantidade=quantidade,
                saida=saida,
                quantidadeAposSaida=quantidade_apos_saida,
                data=data_obj,
                setor=setor
            )

            db.session.add(novo_produto)
            db.session.commit()

            return novo_produto.serialize(), 201

        except Exception as e:
            db.session.rollback()
            return {'message': f'Ocorreu um erro ao criar o produto: {str(e)}'}, 500

    @swag_from({
        'tags': ['Produtos'],
        'summary': 'Atualizar um produto',
        'description': 'Atualiza um produto existente com base no código.',
        'security': [{'BearerAuth': []}],
        'parameters': [
            {
                'name': 'codigo_produto',
                'in': 'path',
                'required': True,
                'type': 'string',
                'description': 'Código do produto a ser atualizado.'
            },
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'nome': {'type': 'string', 'example': 'Produto Atualizado'},
                        'quantidade': {'type': 'integer', 'example': 550},
                        'saida': {'type': 'integer', 'example': 50},
                        'data': {'type': 'string', 'format': 'date', 'example': '2025-05-27'},
                        'setor': {'type': 'string', 'example': 'Expedição'}
                    }
                }
            }
        ],
        'responses': {
            200: {
                'description': 'Produto atualizado com sucesso',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'codigo': {'type': 'string'},
                        'nome': {'type': 'string'},
                        'quantidade': {'type': 'integer'},
                        'saida': {'type': 'integer'},
                        'quantidadeAposSaida': {'type': 'integer'},
                        'data': {'type': 'string', 'format': 'date'},
                        'setor': {'type': 'string'}
                    }
                }
            },
            400: {'description': 'Dados inválidos'},
            401: {'description': 'Usuário não autenticado'},
            404: {'description': 'Produto não encontrado'},
            500: {'description': 'Erro interno do servidor'}
        }
    })
    @jwt_required()
    def put(self, codigo_produto):
        try:
            from src.models import Produto, db # Importação local
            produto = Produto.query.get(codigo_produto)
            if not produto:
                return {'message': f'Produto com código {codigo_produto} não encontrado.'}, 404

            args = produto_parser.parse_args()

            updated = False
            if args['nome'] is not None:
                produto.nome = args['nome']
                updated = True
            if args['quantidade'] is not None:
                if args['quantidade'] < produto.saida:
                    return {'message': 'A nova quantidade não pode ser menor que a saída atual.'}, 400
                produto.quantidade = args['quantidade']
                updated = True
            if args['saida'] is not None:
                if args['saida'] > produto.quantidade:
                    return {'message': 'A nova saída não pode ser maior que a quantidade atual.'}, 400
                produto.saida = args['saida']
                updated = True
            if args['data'] is not None:
                try:
                    produto.data = date.fromisoformat(args['data'])
                    updated = True
                except ValueError:
                    return {'message': 'Formato de data inválido. Use YYYY-MM-DD.'}, 400
            if args['setor'] is not None:
                produto.setor = args['setor']
                updated = True

            if args['quantidade'] is not None or args['saida'] is not None:
                produto.quantidadeAposSaida = produto.quantidade - produto.saida
                updated = True

            if updated:
                db.session.commit()
                return produto.serialize(), 200
            else:
                return {'message': 'Nenhum dado para atualização fornecido.'}, 200

        except Exception as e:
            db.session.rollback()
            return {'message': f'Ocorreu um erro ao atualizar o produto: {str(e)}'}, 500