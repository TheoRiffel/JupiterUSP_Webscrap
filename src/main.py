import sys
from typing import Optional, List
from selenium import webdriver

from scrapper import Scrapper
from Unidade import Unidade


def listar_cursos(unidades: List[Unidade]) -> None:
    for u in unidades:
        print(f"Unidade: {u.nome}")
        for c in u.cursos:
            print("\n".join([" " * 2 + s for s in str(c).split("\n")]))

def listar_dados_curso(unidades: List[Unidade], curso: str):
    for u in unidades:
        print(f"Unidade: {u.nome}")
        for c in u.cursos:
            if curso == c.nome:
                print(curso)


def main() -> None:
    limit: Optional[int] = int(sys.argv[1]) if len(sys.argv) > 1 else None

    scrapper = Scrapper(timeout=8)

    unidades = scrapper.scrape_unidades(limit)

    print(
        f"""\nDigite a opção de consulta:
            1) Lista de cursos por unidades
            2) Dados de um determinado curso
            3) Dados de todos os cursos 
            4) Dados de uma disciplina, inclusive quais cursos ela faz parte
            5) Disciplinas que são usadas em mais de um curso
        """
    )

    print("\33[2K\r", flush=True, end="")

    opcao

    listar_cursos(unidades)
    listar_dados_curso(unidades, nome_curso)

    scrapper.close()


if __name__ == "__main__":
    main()
