class Produto:
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
