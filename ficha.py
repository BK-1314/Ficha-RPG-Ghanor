class Atributo:
    """
    Classe para representar um atributo de um personagem.
    """
    def __init__(self, nome, valor):
        self.nome = nome
        self.valor_base = valor

    def __str__(self):
        return f"{self.nome}: {self.valor_base}"

    def __add_atributo__(self, valor):
        self.valor_base += valor

    def __sub_atributo__(self, valor):
        self.valor_base -= valor

    def __get_atributo__(self):
        return self.valor_base



