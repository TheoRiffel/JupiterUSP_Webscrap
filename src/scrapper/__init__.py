import sys
from typing import List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait

from Unidade import Unidade
from Disciplina import Disciplina, ModalidadeDisciplina
from Curso import Curso
from scrapper.HomePage import HomePage
from scrapper.ResultsPage import ResultsPage
from scrapper.utils import get_int, wait_for_optional_element


class Scrapper:
    def __init__(self, options: Optional[Options] = None, timeout: float = 10, max_workers: int = 10) -> None:
        self.timeout = timeout
        self.max_workers = max_workers
        # Store the base options to create new driver instances in each thread
        self.base_options = options or self._default_options()

    """Worker function to scrape details for a single course."""
    def _scrape_unico_curso(self, curso: Curso) -> None:
        """
        Worker function to scrape details for a single course.
        Each thread running this function will have its own WebDriver instance.
        """
        driver = webdriver.Chrome(options=self.base_options)
        driver.implicitly_wait(self.timeout)
        wait = WebDriverWait(driver, timeout=self.timeout)
        home_page = HomePage(driver, wait)
        results_page = ResultsPage(driver, wait)

        try:
            print(f"  [STARTING] Scraping: {curso.unidade.nome} -> {curso.nome}")
            home_page.open()
            home_page.select_unidade(curso.unidade.nome)
            home_page.select_curso(curso.nome)
            home_page.click_search()

            try:
                home_page.go_to_grade()
            except Exception:
                print(f"\n[ERROR] Não foi possível acessar a grade curricular do curso {curso.nome}.")
                if wait_for_optional_element(driver, home_page.LOCATOR_CLOSE_ERROR_MODAL, timeout=1.5):
                    home_page.close_error_modal()
                return None

            # Screape detalhes do curso
            ideal, minima, maxima = results_page.read_durations()
            curso.duracao_ideal, curso.duracao_minima, curso.duracao_maxima = (
                ideal,
                minima,
                maxima,
            )

            # Scrape disciplinas
            obrig = results_page.get_table("Disciplinas Obrigatórias")
            curso.disciplinas = self._parse_disciplina_table(
                obrig, ModalidadeDisciplina.OBRIGATORIA
            )

            grade_curricular_text = driver.find_element(*ResultsPage.LOCATOR_GRADE).text
            if "Disciplinas Optativas Livres" in grade_curricular_text:
                livres = results_page.get_table("Disciplinas Optativas Livres")
                curso.disciplinas += self._parse_disciplina_table(
                    livres, ModalidadeDisciplina.LIVRE
                )

            if "Disciplinas Optativas Eletivas" in grade_curricular_text:
                eletivas = results_page.get_table("Disciplinas Optativas Eletivas")
                curso.disciplinas += self._parse_disciplina_table(
                    eletivas, ModalidadeDisciplina.ELETIVA
                )
            
            print(f"  [DONE] Processado: {curso.unidade.nome} -> {curso.nome}")

        except Exception as e:
            print(f"[ERROR] A thread falhou pra esse curso: {curso.nome}: {e}", file=sys.stderr)
        finally:
            driver.quit()

    """Scrapa todas as unidades e seus cursos em paralelo.
    Este método primeiro coleta todas as unidades e seus cursos, depois usa um ThreadPoolExecutor
    para scrapar os detalhes de cada curso em paralelo."""
    def scrape_unidades(self, limit: Optional[int] = None) -> List[Unidade]:

        # Step 1: Use a temporary driver to get the list of all units and courses.
        list_driver = webdriver.Chrome(options=self.base_options)
        list_driver.implicitly_wait(self.timeout)
        home_page = HomePage(list_driver, WebDriverWait(list_driver, self.timeout))
        
        all_cursos_to_scrape: List[Curso] = []
        unidades: List[Unidade] = []

        try:
            home_page.open()
            unidade_names = home_page.get_unidades_names()[:limit]
            unidades = [Unidade(n) for n in unidade_names]
            
            print(f"Encontrados {len(unidades)} Unidades. Extraindo cursos ...")
            for unidade in unidades:
                self._print_status_unidades(unidade) 
                home_page.select_unidade(unidade.nome)
                curso_names = home_page.get_cursos()
                # Create Curso objects; they will be populated by the workers
                unidade.cursos = [Curso(name, unidade) for name in curso_names]
                all_cursos_to_scrape.extend(unidade.cursos)
        finally:
            list_driver.quit()
        
        print(f"\nEncontrado um total de {len(all_cursos_to_scrape)} cursos. Começando o scrapping parelelizado...")

        # Step 2: Use a ThreadPoolExecutor to scrape course details in parallel.
        # The worker function modifies the Curso objects in place.
        with ThreadPoolExecutor(self.max_workers) as executor:
            futures = [executor.submit(self._scrape_unico_curso, curso) for curso in all_cursos_to_scrape]
            # Wait for all futures to complete and handle exceptions
            for future in as_completed(futures):
                try:
                    future.result()  # result() will re-raise any exception caught in the worker
                except Exception as e:
                    print(f"[ERROR] Uma tarefa da thread falhou: {e}", file=sys.stderr)

        self._print_successful_parsing(len(unidades))
        return unidades

    def _print_status_unidades(
        self, current_unidade: Unidade
    ) -> None:
        # The old progress bar with '\r' doesn't work with multithreading.
        # A simple print is better.
        print(f"[INFO] Fetching cursos da unidade: {current_unidade.nome}")

    def _print_successful_parsing(self, total_units: int) -> None:
        print("\n" + "#"*16)
        print(f"Parseamento concluído. {total_units} unidade(s) processada(s).")
        print("#"*16 + "\n")

    def _parse_disciplina_table(
        self, table, modalidade: ModalidadeDisciplina
    ) -> List[Disciplina]:
        rows = table.find_elements(
            "xpath", ".//tr[.//a[contains(@class,'disciplina')]]"
        )
        parsed: List[Disciplina] = []
        for row in rows:
            # This logic remains the same as it's efficient enough.
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
    
    def close(self) -> None:
        self.base_options = None
        return None