from Curso import Curso
from Disciplina import Disciplina
from Unidade import Unidade
from utils import get_value_or_none


class Repository:
    def __init__(self, unidades: list[Unidade]) -> None:
        self.unidades = unidades

    def get_unidade_by_name(self, name: str) -> Unidade | None:
        return get_value_or_none([u for u in self.unidades if u.nome == name], 0)

    def get_curso_by_name(self, name: str) -> Curso | None:
        cursos: list[Curso] = []
        for u in self.unidades:
            cursos += u.cursos

        return get_value_or_none([c for c in cursos if c.nome == name], 0)

    def get_disciplinas(self) -> list[Disciplina]:
        cursos: list[Curso] = []
        for u in self.unidades:
            cursos += u.cursos

        disciplinas: list[Disciplina] = []
        for c in cursos:
            disciplinas += c.disciplinas

        return disciplinas

    def get_disciplina_by_name_or_code(self, name_or_code: str) -> Disciplina | None:
        disciplinas = self.get_disciplinas()

        return get_value_or_none(
            [
                d
                for d in disciplinas
                if d.nome == name_or_code or d.codigo == name_or_code
            ],
            0,
        )

    def get_cursos_disciplina(self, disciplina: Disciplina) -> list[Curso]:
        cursos: list[Curso] = []
        for u in self.unidades:
            cursos += u.cursos

        return [c for c in cursos if disciplina in c.disciplinas]

    def get_multiple_cursos_disciplinas(self) -> list[tuple[Disciplina, int]]:
        cursos: list[Curso] = []
        for u in self.unidades:
            cursos += u.cursos

        disciplinas: dict[str, tuple[Disciplina, int]] = {}
        for c in cursos:
            for d in c.disciplinas:
                if d.codigo in disciplinas:
                    disciplinas[d.codigo] = (d, disciplinas[d.codigo][1] + 1)
                else:
                    disciplinas[d.codigo] = (d, 1)

        return [
            disciplinas[codigo] for codigo in disciplinas if disciplinas[codigo][1] >= 2
        ]
