import time
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC

from scrapper.utils import safe_click, wait_for_optional_element


class HomePage:
    LOCATOR_TAB_GRADE = (By.ID, "step4-tab")
    LOCATOR_UNIDADE = (By.ID, "comboUnidade")
    LOCATOR_CURSO = (By.ID, "comboCurso")
    LOCATOR_BTN_ENVIAR = (By.ID, "enviar")
    LOCATOR_CLOSE_ERROR_MODAL = (
        By.XPATH,
        "//html//body//div[7]//div[3]//div//button//span[contains(text(), 'Fechar')]",
    )

    def __init__(self, driver: WebDriver, wait: WebDriverWait) -> None:
        self.driver = driver
        self.wait = wait

    def open(self) -> None:
        self.driver.get(
            "https://uspdigital.usp.br/jupiterweb/jupCarreira.jsp?codmnu=8275"
        )
        self.wait.until(EC.presence_of_element_located(self.LOCATOR_UNIDADE))

    def get_unidades_names(self) -> list[str]:
        select = Select(self.driver.find_element(*self.LOCATOR_UNIDADE))
        self.wait.until(lambda _: len(select.options) > 1)
        return [o.text for o in select.options if o.text]

    def select_unidade(self, nome: str) -> None:
        Select(self.driver.find_element(*self.LOCATOR_UNIDADE)).select_by_visible_text(
            nome
        )

    def get_cursos(self) -> list[str]:
        select = Select(self.driver.find_element(*self.LOCATOR_CURSO))
        self.wait.until(lambda _: len(select.options) > 1)
        return [o.text for o in select.options if o.text]

    def select_curso(self, nome: str) -> None:
        Select(self.driver.find_element(*self.LOCATOR_CURSO)).select_by_visible_text(
            nome
        )

    def click_search(self) -> None:
        safe_click(self.driver.find_element(*self.LOCATOR_BTN_ENVIAR), self.wait)

    def go_to_grade(self) -> None:
        if wait_for_optional_element(
            self.driver, self.LOCATOR_CLOSE_ERROR_MODAL, timeout=1.2
        ):
            raise Exception("Unable to search course.")

        safe_click(self.driver.find_element(*self.LOCATOR_TAB_GRADE), self.wait)

    def close_error_modal(self) -> None:
        safe_click(self.driver.find_element(*self.LOCATOR_CLOSE_ERROR_MODAL), self.wait)
