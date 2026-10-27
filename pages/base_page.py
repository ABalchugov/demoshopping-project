import allure
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from seleniumpagefactory.Pagefactory import PageFactory


class BasePage(PageFactory):

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
            message="Не появилось видимое уведомление с текстом",
        )
