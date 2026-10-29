from decimal import Decimal

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
            "pagination_buttons_locator": ('css', "#pagination > button"),
            "active_page_locator": ('css', "#pagination > button.active"),
            "page_button_locator": ('css', "#pagination > button:nth-child({page_number})"),
            "active_page_button_locator": ('css', "#pagination > button:nth-child({page_number}).active"),
            "first_card_in_product_list_locator": ('xpath', '//*[@id="product-list"]/div[1]')
        }

    def _get_locator(self, name, **values):
        locator_type, value = self.locators[name]
        return self.TYPE_OF_LOCATORS[locator_type.lower()], value.format(**values)

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

    @allure.step("Получить номера страниц каталога")
    def get_page_numbers(self) -> list[int]:
        buttons = self.driver.find_elements(*self._get_locator("pagination_buttons_locator"))
        return [int(button.text) for button in buttons]

    @allure.step("Перейти на страницу каталога {page_number}")
    def go_to_page(self, page_number: int, timeout=10) -> None:
        if page_number < 1:
            raise ValueError("Номер страницы должен быть положительным")

        button = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(
                self._get_locator("page_button_locator", page_number=page_number)
            )
        )
        if "active" in (button.get_attribute("class") or "").split():
            return

        previous_cards = self.get_cards()
        button.click()
        self.wait_for_catalog_updated(previous_cards, timeout=timeout)
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(
                self._get_locator("active_page_button_locator", page_number=page_number)
            )
        )

    @allure.step("Получить параметры товаров со всех страниц каталога")
    def get_all_card_parameters(self) -> list[dict]:
        page_numbers = self.get_page_numbers()
        if not page_numbers:
            return list(map(self.get_card_parameters, self.get_cards()))

        original_page = int(
            self.driver.find_element(*self._get_locator("active_page_locator")).text
        )
        parameters = []
        try:
            for page_number in page_numbers:
                self.go_to_page(page_number)
                parameters.extend(map(self.get_card_parameters, self.get_cards()))
        finally:
            self.go_to_page(original_page)

        return parameters

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
                parameters["price"] = Decimal(
                    text.replace("Цена:", "")
                    .replace("USD", "")
                    .strip()
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
