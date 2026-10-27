import allure
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from pages.base_page import BasePage
from utils.config import TEST_UI_URL


class LoginPage(BasePage):

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)
        self.url = f"{TEST_UI_URL}/login"
        self.locators = {
            "login_locator": ('ID', "login-username"),
            "password_locator": ('ID', "login-password"),
            "login_button_locator": ('xpath', '//*[@id="login-form"]/button'),
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

    @allure.step("Нажать кнопку Войти")
    def click_login_button(self):
        self.login_button_locator.click()

    @allure.step("Проверить редирект при логине")
    def is_redirected(self):
        try:
            self.wait.until(
                EC.url_to_be(f"{TEST_UI_URL}/")
            )
            return True
        except TimeoutException:
            return False
