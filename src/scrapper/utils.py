import time
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.wait import POLL_FREQUENCY
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver


def safe_click(element: WebElement, wait: WebDriverWait, retries=5, delay=0.5):
    for _ in range(retries):
        try:
            overlay_locator = (By.CSS_SELECTOR, "div.blockUI.blockOverlay")
            wait.until(
                lambda _: EC.element_to_be_clickable(element)
                and EC.invisibility_of_element_located(overlay_locator)
            )
            element.click()

            return
        except ElementClickInterceptedException:
            time.sleep(delay)

    element.click()


def get_int(text: str | None) -> int:
    try:
        return int(text.strip())  # type: ignore
    except (ValueError, TypeError):
        return 0


def wait_for_optional_element(
    driver: WebDriver, locator: tuple[str, str], timeout: float = 1
) -> bool:
    original_implicit_wait = driver.timeouts.implicit_wait
    driver.implicitly_wait(0)
    try:
        WebDriverWait(
            driver, timeout, poll_frequency=min(timeout, POLL_FREQUENCY)
        ).until(
            EC.presence_of_element_located(locator),
        )

        driver.implicitly_wait(original_implicit_wait)
        return True
    except TimeoutException:
        driver.implicitly_wait(original_implicit_wait)
        return False
