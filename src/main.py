from enum import Enum, auto
import time
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select
from Unidade import Unidade
from Disciplina import Disciplina
from Curso import Curso
import sys

ID_SELECT_UNIDADE = 'comboUnidade'
ID_SELECT_CURSO = 'comboCurso'

class ModalidadeDisciplina(Enum):
    OBRIGATORIA = auto()
    LIVRE = auto()
    ELETIVA = auto()


def get_select_options(driver: WebDriver, id):
    # Find the select element by its ID
    select_element = Select(driver.find_element(By.ID, id))

    wait = WebDriverWait(driver, timeout=10)
    wait.until(lambda _: len(select_element.options) > 1)

    # Get all option elements within the select element
    options = select_element.options

    return [option.text for option in options if option.text != '']

def get_int_value_from_element(element):
    try:
        return int(element.get_attribute("textContent").strip())
    except ValueError:
        return 0



def parse_disciplinas_table(disciplina_table, modalidade):
    # tabela que tem linha com texto "Disciplinas Obrigatórias"
    # pega as linhas de disciplinas da tabela, onde uma linha que contém um link com uma classe 'disciplina'
    disciplina_rows = disciplina_table.find_elements(By.XPATH, ".//tr[.//a[contains(@class, 'disciplina')]]")
    disciplinas = []
    for row in disciplina_rows:
        # pega o link da disciplina

        codigo = row.find_element(By.XPATH, ".//td[1]").text
        nome = row.find_element(By.XPATH, ".//td[2]").text
        modalidade = modalidade
        creditos_aula = get_int_value_from_element(row.find_element(By.XPATH, ".//td[3]"))
        creditos_trabalho = get_int_value_from_element(row.find_element(By.XPATH, ".//td[4]"))
        carga_horaria = get_int_value_from_element(row.find_element(By.XPATH, ".//td[5]"))
        carga_horaria_estagio = get_int_value_from_element(row.find_element(By.XPATH, ".//td[6]"))
        carga_horaria_praticas = get_int_value_from_element(row.find_element(By.XPATH, ".//td[7]"))
        atividades_teorico_praticas = row.find_element(By.XPATH, ".//td[8]").text

        disciplinas.append(Disciplina(nome, codigo, modalidade, creditos_aula, creditos_trabalho,
                                       carga_horaria, carga_horaria_estagio, carga_horaria_praticas,
                                       atividades_teorico_praticas))

    return disciplinas

limit = int(sys.argv[1]) if len(sys.argv) > 1 else None

driver = webdriver.Chrome()
wait = WebDriverWait(driver, timeout=10)
driver.implicitly_wait(15)
driver.get('https://uspdigital.usp.br/jupiterweb/jupCarreira.jsp?codmnu=8275')
unidades = [Unidade(nome) for nome in get_select_options(driver, ID_SELECT_UNIDADE)[:limit]]

for unidade in unidades:
    Select(driver.find_element(By.ID, ID_SELECT_UNIDADE)).select_by_visible_text(unidade.nome)

    unidade.cursos = [Curso(nome, unidade) for nome in get_select_options(driver, ID_SELECT_CURSO)]
    for curso in unidade.cursos:
        Select(driver.find_element(By.ID, ID_SELECT_CURSO)).select_by_visible_text(curso.nome)

        print(f'Unidade: {unidade.nome}, Curso: {curso.nome}')
        submit_button_id = 'enviar'
        submit_button = driver.find_element(By.ID, submit_button_id)
        submit_button.click()

        grade_curricular_button_id = 'step4-tab'
        grade_curricular_button = driver.find_element(By.ID, grade_curricular_button_id)
        wait.until(lambda _: grade_curricular_button.is_displayed())
        grade_curricular_button.click()

        wait.until(lambda _: driver.find_element(By.CSS_SELECTOR, '.duridlhab').get_attribute("textContent") != '')

        curso.duracao_ideal = get_int_value_from_element(driver.find_element(By.CSS_SELECTOR, '.duridlhab'))
        curso.duracao_minima = get_int_value_from_element(driver.find_element(By.CSS_SELECTOR, '.durminhab'))
        curso.duracao_maxima = get_int_value_from_element(driver.find_element(By.CSS_SELECTOR, '.durmaxhab'))

        # tabela das disciplinas obrigatorias
        grade_curricular = driver.find_element(By.ID, 'gradeCurricular')

        xpath_string = lambda nome: f".//table[.//td[contains(text(), '{nome}')]]"

        disciplinas_obrigatorias = grade_curricular.find_element(By.XPATH, xpath_string("Disciplinas Obrigatórias"))
        curso.disciplinas = parse_disciplinas_table(disciplinas_obrigatorias, ModalidadeDisciplina.OBRIGATORIA)

        # tabela das disciplinas livres
        if "Disciplinas Optativas Livres" in grade_curricular.text:
            disciplinas_livres = grade_curricular.find_element(By.XPATH, xpath_string("Disciplinas Optativas Livres"))
            curso.disciplinas += parse_disciplinas_table(disciplinas_livres, ModalidadeDisciplina.LIVRE)

        # tabela das disciplinas eletivas
        if "Disciplinas Optativas Eletivas" in grade_curricular.text:
            disciplinas_eletivas = grade_curricular.find_element(By.XPATH, xpath_string("Disciplinas Optativas Eletivas"))
            curso.disciplinas += parse_disciplinas_table(disciplinas_eletivas, ModalidadeDisciplina.ELETIVA)

        # Volta para a página anterior
        buscar_button_id = 'step1-tab'
        buscar_button = driver.find_element(By.ID, buscar_button_id)
        wait.until(lambda _: buscar_button.is_displayed())
        buscar_button.click()

driver.quit()

def listar_cursos(unidades):
    for unidade in unidades:

        print(f'Unidade: {unidade.nome}')
        for curso in unidade.cursos:
            print(curso)

listar_cursos(unidades)

