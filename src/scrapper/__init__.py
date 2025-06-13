from typing import List, Optional
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait

from Unidade import Unidade
from Disciplina import Disciplina, ModalidadeDisciplina
from Curso import Curso
from scrapper.HomePage import HomePage
from scrapper.ResultsPage import ResultsPage
from scrapper.utils import get_int


class Scrapper:
    def __init__(self, options: Optional[Options] = None, timeout: float = 10) -> None:
        opts = options or self._default_options()
        self.driver = webdriver.Chrome(opts)
        self.driver.implicitly_wait(timeout)
        self.wait = WebDriverWait(self.driver, timeout=timeout)
        self.home_page = HomePage(self.driver, self.wait)
        self.results_page = ResultsPage(self.driver, self.wait)

    def close(self) -> None:
        self.driver.quit()

    def scrape_unidades(self, limit: Optional[int] = None) -> List[Unidade]:
        self.home_page.open()

        unidade_names = self.home_page.get_unidades_names()[:limit]
        unidades = [Unidade(n) for n in unidade_names]
        total_unidades = len(unidades)

        for i, u in enumerate(unidades):
            self._print_status_unidades(i, u, total_unidades)

            self.home_page.select_unidade(u.nome)
            names = self.home_page.get_cursos()
            u.cursos = [Curso(n, u) for n in names]

            for j, c in enumerate(u.cursos):
                self._print_status_cursos(j, len(u.cursos), c)

                self.home_page.select_curso(c.nome)
                self.home_page.click_search()

                try:
                    self.home_page.go_to_grade()
                except:
                    print("\33[2K\r", flush=True, end="")
                    print(
                        f"\n[ERRO] Não foi possível acessar a grade curricular do curso {c.nome}."
                    )
                    self.home_page.close_error_modal()
                    continue

                ideal, minima, maxima = self.results_page.read_durations()
                c.duracao_ideal, c.duracao_minima, c.duracao_maxima = (
                    ideal,
                    minima,
                    maxima,
                )

                obrig = self.results_page.get_table("Disciplinas Obrigatórias")
                c.disciplinas = self._parse_disciplina_table(
                    obrig, ModalidadeDisciplina.OBRIGATORIA
                )

                grade_curricular_text = self.driver.find_element(
                    *ResultsPage.LOCATOR_GRADE
                ).text
                if "Disciplinas Optativas Livres" in grade_curricular_text:
                    livres = self.results_page.get_table("Disciplinas Optativas Livres")
                    c.disciplinas += self._parse_disciplina_table(
                        livres, ModalidadeDisciplina.LIVRE
                    )

                if "Disciplinas Optativas Eletivas" in grade_curricular_text:
                    eletivas = self.results_page.get_table(
                        "Disciplinas Optativas Eletivas"
                    )
                    c.disciplinas += self._parse_disciplina_table(
                        eletivas, ModalidadeDisciplina.ELETIVA
                    )

                self.results_page.back_to_search()

        self._print_successful_parsing(len(unidades))

        return unidades

    def _print_status_unidades(
        self, index: int, current_unidade: Unidade, total_unidades: int
    ) -> None:
        print("\33[2K\r", flush=True, end="")
        print(f"[Unidade {index+1}/{total_unidades}] {current_unidade.nome}")

    def _print_status_cursos(
        self,
        index: int,
        current_unidade_total_courses: int,
        current_course: Curso,
    ) -> None:
        print("\33[2K\r", flush=True, end="")
        print(
            f"  [Curso {index+1}/{current_unidade_total_courses}] {current_course.nome}",
            end="",
            flush=True,
        )

    def _print_successful_parsing(self, total_units: int) -> None:
        print("\33[2K\r", flush=True, end="")

        print("\n################")
        print(f"Parseamento concluído. {total_units} unidade(s) processada(s).")
        print("################\n")

    def _parse_disciplina_table(
        self, table, modalidade: ModalidadeDisciplina
    ) -> List[Disciplina]:
        rows = table.find_elements(
            "xpath", ".//tr[.//a[contains(@class,'disciplina')]]"
        )
        parsed: List[Disciplina] = []
        for row in rows:
            codigo = row.find_element("xpath", ".//td[1]").text
            nome = row.find_element("xpath", ".//td[2]").text
            creditos_aula = get_int(
                row.find_element("xpath", ".//td[3]").get_attribute("textContent")
            )
            creditos_trabalho = get_int(
                row.find_element("xpath", ".//td[4]").get_attribute("textContent")
            )
            carga_horaria = get_int(
                row.find_element("xpath", ".//td[5]").get_attribute("textContent")
            )
            carga_horaria_estagio = get_int(
                row.find_element("xpath", ".//td[6]").get_attribute("textContent")
            )
            carga_horaria_praticas = get_int(
                row.find_element("xpath", ".//td[7]").get_attribute("textContent")
            )
            atividades_teorico_praticas = row.find_element("xpath", ".//td[8]").text
            parsed.append(
                Disciplina(
                    nome,
                    codigo,
                    modalidade,
                    creditos_aula,
                    creditos_trabalho,
                    carga_horaria,
                    carga_horaria_estagio,
                    carga_horaria_praticas,
                    atividades_teorico_praticas,
                )
            )
        return parsed

    def _default_options(self) -> Options:
        opts = webdriver.ChromeOptions()
        opts.add_argument("--headless=new")
        opts.add_argument("--disable-gpu")
        opts.add_argument("--window-size=1920,1080")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_experimental_option("excludeSwitches", ["enable-automation"])
        opts.add_experimental_option("useAutomationExtension", False)
        opts.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
        )
        return opts
