class Curso():
    def __init__(self, nome, unidade, duracao_ideal=0, duracao_minima=0, duracao_maxima=0, disciplinas = []):
        self.nome = nome
        self.unidade = unidade
        self.duracao_ideal = duracao_ideal
        self.duracao_minima = duracao_minima
        self.duracao_maxima = duracao_maxima   
        self.disciplinas = disciplinas

    def __str__(self):
        return f'Curso: {self.nome}, Unidade: {self.unidade.nome}, Duração Ideal: {self.duracao_ideal}, Duração Mínima: {self.duracao_minima}, Duração Máxima: {self.duracao_maxima}, Disciplinas: {len(self.disciplinas)}'
