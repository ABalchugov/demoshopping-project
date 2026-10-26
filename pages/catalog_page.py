import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
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
            "cards_locator": ('css', "#product-list > div"),
            "first_card_in_product_list_locator": ('xpath', '//*[@id="product-list"]/div[1]')
        }

    def _get_locator(self, name):
        locator_type, value = self.locators[name]
        return self.TYPE_OF_LOCATORS[locator_type.lower()], value

    @allure.step("Открыть каталог")
    def open(self):
        self.driver.get(self.url)

    @allure.step("Дождаться первичной загрузки каталога")
    def wait_for_catalog_loaded(self, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_all_elements_located(self._get_locator("cards_locator"))
        )

    @allure.step("Дождаться обновления каталога")
    def wait_for_catalog_updated(self, previous_cards: list[WebElement], timeout=10) -> None:
        if not previous_cards:
            raise ValueError("До обновления в каталоге должна быть хотя бы одна карточка")

        WebDriverWait(self.driver, timeout).until(
            EC.staleness_of(previous_cards[0])
        )

    @allure.step("Получить карточки каталога")
    def get_cards(self) -> list[WebElement]:
        return self.driver.find_elements(*self._get_locator("cards_locator"))

    @allure.step("Получить первую карточку")
    def get_first_card(self):
        cards = self.get_cards()

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
