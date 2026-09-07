import allure
from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from seleniumpagefactory.Pagefactory import PageFactory, ElementNotFoundException
from selenium.webdriver.support import expected_conditions as EC
import os


class LoginPage(PageFactory):

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)
        self.url = f'{os.getenv("TEST_UI_URL")}/login'
        self.locators = {
            "login_locator": ('ID', "login-username"),
            "password_locator": ('ID', "login-password"),
            "login_button_locator": ('xpath', '//*[@id="login-form"]/button'),
            "wrong_login_msg_locator": ('xpath',
                                        "//div[text()='Логин должен содержать от 3 до 15 символов и может включать буквы, цифры и символы: _']"),
            "wrong_password_msg_locator": ('xpath',
                                           "//div[text()='Пароль должен содержать не менее 8 символов, включая минимум одну букву и одну цифру']"),
            "wrong_login_and_password_msg_locator": ('xpath',
                                                     "//div[contains(., 'Логин должен содержать от 3 до 15 символов') and contains(., 'Пароль должен содержать не менее 8 символов')]"),
            "server_error_msg_locator": ('xpath', "//div[text()='Произошла ошибка при обработке запроса']"),
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

    @allure.step("Нажать кнопку Войти")
    def click_login_button(self):
        self.login_button_locator.click()

    @allure.step("Проверить сообщение об ошибке в поле Логин")
    def wrong_login_msg_is_displayed(self):
        try:
            return self.wait.until(
                lambda driver: self.wrong_login_msg_locator.is_displayed()
            )
        except TimeoutException, ElementNotFoundException:
            return False

    @allure.step("Проверить сообщение об ошибке в поле Пароль")
    def wrong_password_msg_is_displayed(self):
        try:
            return self.wait.until(
                lambda driver: self.wrong_password_msg_locator.is_displayed()
            )
        except TimeoutException, ElementNotFoundException:
            return False

    @allure.step("Проверить сообщение об ошибке в полях Логин и Пароль")
    def wrong_login_and_password_msg_is_displayed(self):
        try:
            return self.wait.until(
                lambda driver: self.wrong_login_and_password_msg_locator.is_displayed()
            )
        except TimeoutException, ElementNotFoundException:
            return False

    @allure.step("Проверить сообщение при попытке логина с несуществующими данными")
    def non_existed_user_msg_is_displayed(self):
        try:
            return self.wait.until(
                lambda driver: self.server_error_msg_locator.is_displayed()
            )
        except TimeoutException, ElementNotFoundException:
            return False

    @allure.step("Проверить редирект при логине")
    def is_redirected(self):
        try:
            self.wait.until(
                EC.url_to_be(f'{os.getenv("TEST_UI_URL")}/')
            )
            return True
        except TimeoutException, ElementNotFoundException:
            return False
