import allure
from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from seleniumpagefactory.Pagefactory import PageFactory
import os


class RegistrationPage(PageFactory):

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)
        self.url = f'{os.getenv("TEST_URL")}/login'
        self.locators = {
            "login_locator": ('ID', "register-username"),
            "password_locator": ('ID', "register-password"),
            "registration_button_locator": ('xpath', '//*[@id="register-form"]/button'),
            "wrong_login_msg_locator": ('xpath',
                                        "//div[text()='Логин должен содержать от 3 до 15 символов и может включать буквы, цифры и символы: _']"),
            "wrong_password_msg_locator": ('xpath',
                                           "//div[text()='Пароль должен содержать не менее 8 символов, включая минимум одну букву и одну цифру']"),
            "wrong_login_and_password_msg_locator": ('xpath',
                                                     "//div[contains(., 'Логин должен содержать от 3 до 15 символов') and contains(., 'Пароль должен содержать не менее 8 символов')]"),
            "success_registration_msg_locator": ('xpath', "//div[text()='Регистрация выполнена успешно']")
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

    @allure.step("Проверить сообщение об ошибке в поле Логин")
    def wrong_login_msg_is_displayed(self):
        try:
            return self.wait.until(
                lambda driver: self.wrong_login_msg_locator.is_displayed()
            )
        except TimeoutException:
            return False

    @allure.step("Проверить сообщение об ошибке в поле Пароль")
    def wrong_password_msg_is_displayed(self):
        try:
            return self.wait.until(
                lambda driver: self.wrong_password_msg_locator.is_displayed()
            )
        except TimeoutException:
            return False

    @allure.step("Проверить сообщение об ошибке в полях Логин и Пароль")
    def wrong_login_and_password_msg_is_displayed(self):
        try:
            return self.wait.until(
                lambda driver: self.wrong_login_and_password_msg_locator.is_displayed()
            )
        except TimeoutException:
            return False

    @allure.step("Проверить сообщение об успешной регистрации")
    def success_registration_msg_is_displayed(self):
        try:
            return self.wait.until(
                lambda driver: self.success_registration_msg_locator.is_displayed()
            )
        except TimeoutException:
            return False
