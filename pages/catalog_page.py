import allure
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from seleniumpagefactory.Pagefactory import PageFactory
import os


class CatalogPage(PageFactory):

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)
        self.url = os.getenv("TEST_UI_URL")
        self.locators = {
            "product_list_locator": ('ID', "product-list"),
            "first_card_in_product_list_locator": ('xpath', '//*[@id="product-list"]/div[1]')
        }

    @allure.step("Открыть каталог")
    def open(self):
        self.driver.get(self.url)

    @allure.step("Получить состояние каталога")
    def get_catalog_state(self):
        return self.driver.find_element(By.ID, "product-list").get_attribute("innerHTML")

    @allure.step("Ожидание результата фильтрации")
    def wait_for_filter_result(self, old_state, timeout=5):
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.find_element(By.ID, "product-list").get_attribute("innerHTML") != old_state
            )
        except TimeoutException:
            pass  # список мог не измениться — это нормальный исход

    @allure.step("Получить первую карточку")
    def get_first_card(self):
        cards = self.driver.find_elements(
            By.XPATH,
            '//*[@id="product-list"]/div[1]'
        )

        if not cards:
            return None

        return cards[0]

    @allure.step("Получить параметры первой карточки")
    def get_first_card_parameters(self):
        card = self.get_first_card()

        if card is None:
            return {}

        parameters = {}

        for p in card.find_elements(By.TAG_NAME, "p"):
            text = p.text

            if text.startswith("Цена:"):
                parameters["price"] = int(
                    text.replace("Цена:", "")
                    .replace("USD", "")
                    .strip()
                    .split(".")[0]
                )

            elif text.startswith("Категория:"):
                parameters["category"] = (
                    text.replace("Категория:", "").strip()
                )

            elif text.startswith("Производитель:"):
                parameters["manufacturer"] = (
                    text.replace("Производитель:", "").strip()
                )

            elif text.startswith("Бесплатная доставка:"):
                parameters["free_shipping"] = (
                    text.replace("Бесплатная доставка:", "").strip()
                )

        return parameters
