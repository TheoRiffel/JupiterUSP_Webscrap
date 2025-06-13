from __future__ import annotations
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Curso import Curso


@dataclass
class Unidade:
    nome: str
    cursos: list[Curso] = field(default_factory=list)

    def __str__(self) -> str:
        return (
            f"Unidade:\n"
            f"  Nome: {self.nome}\n"
            f"  Quantidade de Cursos: {len(self.cursos)}"
        )
