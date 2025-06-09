from enum import Enum, auto
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
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
    

def get_select_options(driver, id):
    # Find the select element by its ID
    select_element = driver.find_element(By.ID, id)
    
    # Get all option elements within the select element
    options = select_element.find_elements(By.TAG_NAME, 'option')
    
    return [option.text for option in options if option.text != '']

def get_int_value_from_element(element):
    try:
        return int(element.text.strip())
    except ValueError:
        return 0
    

    
def parse_disciplinas_table(disciplina_table, modalidade):

    print("pinto")
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
    
    print("penis")

    return disciplinas

limit = int(sys.argv[1]) if len(sys.argv) > 1 else None

driver = webdriver.Chrome()
driver.implicitly_wait(10)      
driver.get('https://uspdigital.usp.br/jupiterweb/jupCarreira.jsp?codmnu=8275')
print("aaaaaaaaaaaaaaaaaa")
time.sleep(3)  # wait for the page to load
unidades = [Unidade(nome) for nome in get_select_options(driver, ID_SELECT_UNIDADE)[:limit]]
print(unidades)

for unidade in unidades:
    time.sleep(3)  # wait for the page to load
    unidade.cursos = [Curso(nome, unidade) for nome in get_select_options(driver, ID_SELECT_CURSO)]
    
    print(unidade.cursos)
    driver.find_element(By.ID, ID_SELECT_UNIDADE).send_keys(unidade.nome)
    for curso in unidade.cursos:
        driver.find_element(By.ID, ID_SELECT_CURSO).send_keys(curso.nome)
        
        print(f'Unidade: {unidade.nome}, Curso: {curso.nome}')
        submit_button_id = 'enviar'
        submit_button = driver.find_element(By.ID, submit_button_id)
        submit_button.click()

        grade_curricular_button_id = 'step4-tab'
        grade_curricular_button = driver.find_element(By.ID, grade_curricular_button_id)
        grade_curricular_button.click()

        time.sleep(0.5)  # wait for the page to load

        curso.duracao_ideal = int(driver.find_element(By.CSS_SELECTOR, '.duridlhab').get_attribute("textContent"))
        curso.duracao_minima = int(driver.find_element(By.CSS_SELECTOR, '.durminhab').get_attribute("textContent"))
        curso.duracao_maxima = int(driver.find_element(By.CSS_SELECTOR, '.durmaxhab').get_attribute("textContent"))

        # tabela das disciplinas obrigatorias

        grade_curricular = driver.find_element(By.ID, 'gradeCurricular')
        
        disciplinas_obrigatorias = grade_curricular.find_element(By.XPATH, ".//table[.//td[contains(text(), 'Disciplinas Obrigatórias')]]")
        curso.disciplinas = parse_disciplinas_table(disciplinas_obrigatorias, ModalidadeDisciplina.OBRIGATORIA)

        # tabela das disciplinas livres
        try:
            disciplinas_livres = grade_curricular.find_element(By.XPATH, ".//table[.//td[contains(text(), 'Disciplinas Optativas Livres')]]")
            curso.disciplinas += parse_disciplinas_table(disciplinas_livres, ModalidadeDisciplina.LIVRE)
        except Exception as e:
            pass

        # tabela das disciplinas eletivas
        try:
            disciplinas_eletivas = grade_curricular.find_element(By.XPATH, ".//table[.//td[contains(text(), 'Disciplinas Optativas Eletivas')]]")
            curso.disciplinas += parse_disciplinas_table(disciplinas_eletivas, ModalidadeDisciplina.ELETIVA)
        except Exception as e:
            pass

        print(f'Disciplinas encontradas: {len(curso.disciplinas)}')
        for disciplina in curso.disciplinas:
            print(f'  Disciplina: {disciplina.nome}, Código: {disciplina.codigo}, Modalidade: {disciplina.modalidade.name}, Carga Horária: {disciplina.carga_horaria}')
        
        # Volta para a página anterior
        buscar_button_id = 'step1-tab'
        buscar_button = driver.find_element(By.ID, buscar_button_id)
        buscar_button.click()

driver.quit()

def listar_cursos(unidades):
    for unidade in unidades:

        print(f'Unidade: {unidade.nome}')
        for curso in unidade.cursos:
            print(curso)

listar_cursos(unidades)

