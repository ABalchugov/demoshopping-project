import allure
from selenium.webdriver.support.wait import WebDriverWait
from seleniumpagefactory.Pagefactory import PageFactory
from selenium.webdriver.support.ui import Select
import os


class FilterPage(PageFactory):

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)
        self.url = os.getenv("TEST_URL")
        self.locators = {
            "min_price_locator": ('ID', "min-price"),
            "max_price_locator": ('ID', "max-price"),
            "categories_locator": ('ID', "category"),
            "manufacturer_locator": ('ID', "manufacturer"),
            "free_shipping_checkbox_locator": ('ID', "free-shipping"),
            "apply_filters_button_locator": ('ID', "apply-filters"),
            "reset_filters_button_locator": ('ID', "reset-filters")
        }

    @allure.step("Открыть каталог")
    def open(self):
        self.driver.get(self.url)

    @allure.step("Заполнить поле Мин цена значением: {price}")
    def fill_min_price_filter(self, price):
        self.min_price_locator.set_text(price)

    @allure.step("Заполнить поле Макс цена значением: {price}")
    def fill_max_price_filter(self, price):
        self.max_price_locator.set_text(price)

    @allure.step("Выбрать категорию {category}")
    def choose_categories_filter(self, category):
        select = Select(self.categories_locator)
        select.select_by_value(category)

    @allure.step("Выбрать производителя {manufacturer}")
    def choose_manufacturer_filter(self, manufacturer):
        select = Select(self.manufacturer_locator)
        select.select_by_value(manufacturer)

    @allure.step("Выбрать фильтр бесплатной доставки")
    def click_free_shipping_checkbox_filter(self):
        self.free_shipping_checkbox_locator.click()

    @allure.step("Нажать кнопку Применить фильтр")
    def click_apply_filters_button(self):
        self.apply_filters_button_locator.click()

    @allure.step("Нажать кнопку Сбросить фильтры")
    def click_reset_filters_button(self):
        self.reset_filters_button_locator.click()

    @allure.step("Получить текущее состояние фильтров")
    def get_filters_state(self):
        state = {"min_price": self.min_price_locator.get_attribute("value"),
                 "max_price": self.max_price_locator.get_attribute("value"),
                 "category": self.categories_locator.get_attribute("value"),
                 "manufacturer": self.manufacturer_locator.get_attribute("value"),
                 "free_shipping": self.free_shipping_checkbox_locator.is_selected()}

        return state
