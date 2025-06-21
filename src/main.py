import sys
from typing import NoReturn, Optional, List

from Curso import Curso
from Disciplina import Disciplina, ModalidadeDisciplina
from Repository import Repository
from scrapper import Scrapper
from Unidade import Unidade

MAX_WORKERS_DEFAULT = 10

def exibir_cursos_unidade(unidade: Unidade) -> None:
    print(f"Unidade: {unidade.nome}")
    for c in unidade.cursos:
        print(c.nome)


def exibir_todos_cursos(unidades: list[Unidade]) -> None:
    for u in unidades:
        print(f"Unidade: {u.nome}")
        for c in u.cursos:
            print("\n".join([" " * 2 + s for s in str(c).split("\n")]))


def exibir_disciplina_e_cursos(disciplina: Disciplina, cursos: list[Curso]) -> None:
    print(disciplina)
    print(" " * 2 + "Cursos em que a disciplina está presente:")
    for c in cursos:
        print(" " * 4 + c.nome)


def exibir_multiple_cursos_disciplinas(
    multiple_cursos_disciplinas: list[tuple[Disciplina, int]],
) -> None:
    for d, quantidade in sorted(
        multiple_cursos_disciplinas, key=lambda cursos_disciplina: cursos_disciplina[1]
    )[::-1]:
        print(f"{d.codigo} - {d.nome} | Presente em {quantidade} cursos")


def exibir_disciplinas(disciplinas: list[Disciplina]) -> None:
    for d in disciplinas:
        print(d)


def tear_down(scrapper: Scrapper, status_code=0) -> NoReturn:
    scrapper.close()
    exit(status_code)


def main() -> None:
    limit: Optional[int] = None
    
    try:
        limit = int(sys.argv[1]) if len(sys.argv) > 1 else None
    except ValueError:
        print("Argumento inválido. Deve ser um número inteiro.")
        exit(1) 

    max_workers = int(input("Digite o número máximo de threads (default 10): ").strip() or MAX_WORKERS_DEFAULT)
    if max_workers <= 0:
        print("Número de threads deve ser maior que zero. Utilizando o valor padrão de 10.")
        max_workers = MAX_WORKERS_DEFAULT
  
    scrapper = Scrapper(timeout=8, max_workers=max_workers)

    unidades = scrapper.scrape_unidades(limit)

    repository = Repository(unidades)

    print(
        f"""\nDigite a opção de consulta:
            1) Lista de cursos por unidades
            2) Dados de um determinado curso
            3) Dados de todos os cursos
            4) Dados de uma disciplina, inclusive quais cursos ela faz parte
            5) Disciplinas que são usadas em mais de um curso
            6) Disciplinas com mais de 90 horas de carga horária
            7) Disciplinas de uma modalidade específica (Obrigatória, Livre ou Eletiva)
        """
    )

    opcao = int(input("Digite a opção: ").strip())

    match opcao:
        case 1:
            nome_unidade = input("Digite o nome da unidade: ").strip()
            unidade = repository.get_unidade_by_name(nome_unidade)

            if not unidade:
                print("Unidade não encontrada!")
                tear_down(scrapper, 1)

            exibir_cursos_unidade(unidade)
        case 2:
            nome_curso = input("Digite o nome do curso: ").strip()
            curso = repository.get_curso_by_name(nome_curso)

            if not curso:
                print("Curso não encontrado!")
                tear_down(scrapper, 1)

            print(curso)
        case 3:
            exibir_todos_cursos(unidades)
        case 4:
            nome_codigo_disciplina = input(
                "Digite o nome ou código da disciplina: "
            ).strip()
            disciplina = repository.get_disciplina_by_name_or_code(
                nome_codigo_disciplina
            )

            if not disciplina:
                print("Disciplina não encontrada!")
                tear_down(scrapper, 1)

            cursos_disciplina = repository.get_cursos_disciplina(disciplina)

            exibir_disciplina_e_cursos(disciplina, cursos_disciplina)
        case 5:
            multiple_cursos_disciplinas = repository.get_multiple_cursos_disciplinas()

            exibir_multiple_cursos_disciplinas(multiple_cursos_disciplinas)
        case 6:
            disciplinas = [
                d for d in repository.get_disciplinas() if (d.carga_horaria or 0) >= 90
            ]

            exibir_disciplinas(disciplinas)
        case 7:
            nome_curso = input("Digite o nome do curso: ").strip()
            curso = repository.get_curso_by_name(nome_curso)

            if not curso:
                print("Curso não encontrado!")
                tear_down(scrapper, 1)

            modalide_str = input(
                "Digite a modalidade que deseja buscar (Obrigatória, Livre ou Eletiva): "
            ).strip()

            modalidade = None
            match modalide_str:
                case "Obrigatória":
                    modalidade = ModalidadeDisciplina.OBRIGATORIA
                case "Livre":
                    modalidade = ModalidadeDisciplina.LIVRE
                case "Eletiva":
                    modalidade = ModalidadeDisciplina.ELETIVA
                case _:
                    print(
                        "Modalidade inválida. Escolha entre Obrigatória, Livre ou Eletiva."
                    )
                    tear_down(scrapper, 1)

            disciplinas = [d for d in curso.disciplinas if d.modalidade == modalidade]

            exibir_disciplinas(disciplinas)

    tear_down(scrapper)


if __name__ == "__main__":
    main()
