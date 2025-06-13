from __future__ import annotations
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

from utils import format_none_value

if TYPE_CHECKING:
    from Disciplina import Disciplina
    from Unidade import Unidade


@dataclass
class Curso:
    nome: str
    unidade: Unidade
    duracao_ideal: Optional[int] = None
    duracao_minima: Optional[int] = None
    duracao_maxima: Optional[int] = None
    disciplinas: list[Disciplina] = field(default_factory=list)

    def __str__(self) -> str:
        return (
            f"Curso:\n"
            f"  Nome: {self.nome}\n"
            f"  Unidade: {self.unidade.nome}\n"
            f"  Duração Ideal: {format_none_value(self.duracao_ideal)}\n"
            f"  Duração Mínima: {format_none_value(self.duracao_minima)}\n"
            f"  Duração Máxima: {format_none_value(self.duracao_maxima)}\n"
            f"  Quantidade de Disciplinas: {len(self.disciplinas)}"
        )
