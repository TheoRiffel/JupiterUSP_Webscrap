from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Optional

from utils import format_none_value


class ModalidadeDisciplina(Enum):
    OBRIGATORIA = auto()
    LIVRE = auto()
    ELETIVA = auto()


@dataclass
class Disciplina:
    nome: str
    codigo: str
    modalidade: ModalidadeDisciplina
    creditos_aula: Optional[int]
    creditos_trabalho: Optional[int]
    carga_horaria: Optional[int]
    carga_horaria_estagio: Optional[int]
    carga_horaria_praticas: Optional[int]
    atividades_teorico_praticas: Optional[Any]

    def __str__(self) -> str:
        return (
            f"Disciplina:\n"
            f"  Código: {self.codigo}\n"
            f"  Nome: {self.nome}\n"
            f"  Modalidade: {self.modalidade.name}\n"
            f"  Créditos — Aula: {format_none_value(self.creditos_aula)}, Trabalho: {format_none_value(self.creditos_trabalho)}\n"
            f"  Carga Horária — Total: {format_none_value(self.carga_horaria)}, Estágio: {format_none_value(self.carga_horaria_estagio)}, Práticas: {format_none_value(self.carga_horaria_praticas)}\n"
            f"  Atividades T/P: {format_none_value(self.atividades_teorico_praticas)}"
        )
