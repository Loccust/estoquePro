from src.models.db import db


class Produto(db.Model):
    codigo = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    quantidade = db.Column(db.Integer, default=False, nullable=False)
    saida = db.Column(db.Integer, default=False, nullable=False)
    quantidadeAposSaida = db.Column(db.Integer, default=False, nullable=False)
    data = db.Column(db.Date, default=False, nullable=False)
    setor = db.Column(db.String(25), default=False, nullable=False)

    def __init__(self, codigo, nome, quantidade, saida, quantidadeAposSaida, data, setor):
        self.codigo = codigo
        self.nome = nome
        self.quantidade = quantidade
        self.saida = saida
        self.quantidadeAposSaida = quantidadeAposSaida
        self.data = data
        self.setor = setor

    def serialize(self):
        return {
            "codigo": self.codigo,
            "nome": self.nome,
            "quantidade": self.quantidade,
            "saida": self.saida,
            "quantidadeAposSaida": self.quantidadeAposSaida,
            "data": self.data.isoformat(),
            "setor": self.setor,
        }
