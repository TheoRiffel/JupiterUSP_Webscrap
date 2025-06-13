from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from typing import Tuple
from selenium.webdriver.support import expected_conditions as EC

from scrapper.utils import get_int, safe_click


class ResultsPage:
    LOCATOR_DUR_IDEAL = (By.CSS_SELECTOR, ".duridlhab")
    LOCATOR_DUR_MIN = (By.CSS_SELECTOR, ".durminhab")
    LOCATOR_DUR_MAX = (By.CSS_SELECTOR, ".durmaxhab")
    LOCATOR_GRADE = (By.ID, "gradeCurricular")
    LOCATOR_BACK_BUTTON = (By.ID, "step1-tab")
    XPATH_TABLE = ".//table[.//td[contains(text(), '{label}')]]"

    def __init__(self, driver: WebDriver, wait: WebDriverWait) -> None:
        self.driver = driver
        self.wait = wait

    def read_durations(self) -> Tuple[int, int, int]:
        self.wait.until(
            lambda _: self.driver.find_element(*self.LOCATOR_DUR_IDEAL).get_attribute(
                "textContent"
            )
            != ""
        )
        ideal = get_int(
            self.driver.find_element(*self.LOCATOR_DUR_IDEAL).get_attribute(
                "textContent"
            )
        )
        minimo = get_int(
            self.driver.find_element(*self.LOCATOR_DUR_MIN).get_attribute("textContent")
        )
        maximo = get_int(
            self.driver.find_element(*self.LOCATOR_DUR_MAX).get_attribute("textContent")
        )
        return ideal, minimo, maximo

    def get_table(self, label: str) -> WebElement:
        grade = self.driver.find_element(*self.LOCATOR_GRADE)
        return grade.find_element(By.XPATH, self.XPATH_TABLE.format(label=label))

    def back_to_search(self) -> None:
        safe_click(self.driver.find_element(*self.LOCATOR_BACK_BUTTON), self.wait)
