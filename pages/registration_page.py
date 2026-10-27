import allure

from pages.base_page import BasePage
from utils.config import TEST_UI_URL


class RegistrationPage(BasePage):

    def __init__(self, driver):
        self.driver = driver
        self.url = f"{TEST_UI_URL}/login"
        self.locators = {
            "login_locator": ('ID', "register-username"),
            "password_locator": ('ID', "register-password"),
            "registration_button_locator": ('xpath', '//*[@id="register-form"]/button'),
            "notification_locator": ('css', 'div[style*="animation"]'),
        }

    @allure.step("Открыть форму")
    def open(self):
        self.driver.get(self.url)

    @allure.step("Заполнить поле Логин значением: {login}")
    def fill_login_field(self, login):
        self.login_locator.set_text(login)

    @allure.step("Заполнить поле Пароль значением: {password}")
    def fill_password_field(self, password):
        self.password_locator.set_text(password)

    @allure.step("Нажать кнопку Зарегистрироваться")
    def click_registration_button(self):
        self.registration_button_locator.click()
