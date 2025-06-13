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


def main() -> None:
    limit: Optional[int] = int(sys.argv[1]) if len(sys.argv) > 1 else None

    scrapper = Scrapper(timeout=8)

    unidades = scrapper.scrape_unidades(limit)

    listar_cursos(unidades)

    scrapper.close()


if __name__ == "__main__":
    main()
