import allure
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from seleniumpagefactory.Pagefactory import PageFactory
from utils.config import TEST_UI_URL


class CatalogPage(PageFactory):

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.url = TEST_UI_URL
        self.locators = {
            "product_list_locator": ('ID', "product-list"),
            "first_card_in_product_list_locator": ('xpath', '//*[@id="product-list"]/div[1]')
        }

    @allure.step("Открыть каталог")
    def open(self):
        self.driver.get(self.url)

    @allure.step("Дождаться первичной загрузки каталога")
    def wait_for_catalog_loaded(self, timeout=10):
        def catalog_has_results(driver):
            product_list = driver.find_element(By.ID, "product-list")
            return product_list if product_list.find_elements(By.XPATH, "./div") else False

        return WebDriverWait(self.driver, timeout).until(catalog_has_results)

    @allure.step("Дождаться карточек, соответствующих фильтру")
    def wait_for_filter_result(self, condition, timeout=10):
        def result_matches(driver):
            try:
                card = self.get_first_card()
                return condition(self.get_card_parameters(card))
            except StaleElementReferenceException:
                return False

        return WebDriverWait(self.driver, timeout).until(result_matches)

    @allure.step("Получить первую карточку")
    def get_first_card(self):
        cards = self.driver.find_elements(
            By.XPATH,
            '//*[@id="product-list"]/div[1]'
        )

        if not cards:
            return None

        return cards[0]

    @allure.step("Получить параметры карточки")
    def get_card_parameters(self, card):
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
