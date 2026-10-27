import allure
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from seleniumpagefactory.Pagefactory import PageFactory
from utils.config import TEST_UI_URL


class LoginPage(PageFactory):

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

    @allure.step("Получить текст уведомления")
    def get_notification_text(self, timeout=5) -> str:
        locator_type, value = self.locators["notification_locator"]
        locator = (self.TYPE_OF_LOCATORS[locator_type.lower()], value)
        visible_notification = EC.visibility_of_element_located(locator)

        def read_visible_text(driver) -> str:
            notification = visible_notification(driver)
            return notification.text.strip() if notification else ""

        return WebDriverWait(
            self.driver,
            timeout,
            poll_frequency=0.1,
            ignored_exceptions=(StaleElementReferenceException,),
        ).until(
            read_visible_text,
            message="Не появилось видимое уведомление с текстом на странице входа",
        )

    @allure.step("Проверить редирект при логине")
    def is_redirected(self):
        try:
            self.wait.until(
                EC.url_to_be(f"{TEST_UI_URL}/")
            )
            return True
        except TimeoutException:
            return False
