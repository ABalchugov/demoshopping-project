import allure
import pytest

from pages.login_page import LoginPage


INVALID_LOGIN_MESSAGE = (
    "Логин должен содержать от 3 до 15 символов и может включать буквы, цифры и символы: _"
)
INVALID_PASSWORD_MESSAGE = (
    "Пароль должен содержать не менее 8 символов, включая минимум одну букву и одну цифру"
)
INVALID_LOGIN_AND_PASSWORD_MESSAGE = f"{INVALID_LOGIN_MESSAGE} {INVALID_PASSWORD_MESSAGE}"
AUTHENTICATION_ERROR_MESSAGE = "Произошла ошибка при обработке запроса"


@allure.label("layer", "UI Tests")
@allure.epic("UI Automation")
@allure.feature("Форма логина")
@allure.story("Успешная авторизация")
@allure.title("Отправка формы с корректными данными")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.regress
@pytest.mark.parametrize(
    "login, password",
    [
        ("User171", "somepass1"),
    ],
)
def test_positive_authorization(
        driver,
        login,
        password,
):
    form = LoginPage(driver)

    form.open()
    form.fill_login_field(login)
    form.fill_password_field(password)
    form.click_login_button()

    with allure.step("Проверить редирект на страницу каталога"):
        assert form.is_redirected(), "Редиректа не произошло"


@allure.label("layer", "UI Tests")
@allure.epic("UI Automation")
@allure.feature("Форма логина")
@allure.story("Неуспешная авторизация")
@allure.title("Отправка формы с несуществующими кредами")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.regress
@pytest.mark.parametrize(
    "login, password",
    [
        ("Userjhs171", "somepass1"),
    ],
)
def test_non_existed_user_authorization(
        driver,
        login,
        password,
):
    form = LoginPage(driver)

    form.open()
    form.fill_login_field(login)
    form.fill_password_field(password)
    form.click_login_button()

    notification_text = form.get_notification_text()

    with allure.step("Проверить авторизацию несуществующего пользователя"):
        assert notification_text == AUTHENTICATION_ERROR_MESSAGE, "Неверное сообщение при входе с несуществующими данными"


@allure.label("layer", "UI Tests")
@allure.epic("UI Automation")
@allure.feature("Форма логина")
@allure.story("Неуспешная авторизация")
@allure.title("Отправка формы с некорректным логином")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.regress
@pytest.mark.parametrize(
    "login, password",
    [
        ("User!", "somepass1"),
    ],
)
def test_wrong_login_field_authorization(
        driver,
        login,
        password,
):
    form = LoginPage(driver)

    form.open()
    form.fill_login_field(login)
    form.fill_password_field(password)
    form.click_login_button()

    notification_text = form.get_notification_text()

    with allure.step("Проверить текст уведомления об ошибке логина"):
        assert notification_text == INVALID_LOGIN_MESSAGE, "Неверное сообщение об ошибке логина"


@allure.label("layer", "UI Tests")
@allure.epic("UI Automation")
@allure.feature("Форма логина")
@allure.story("Неуспешная авторизация")
@allure.title("Отправка формы с некорректным паролем")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.regress
@pytest.mark.parametrize(
    "login, password",
    [
        ("User171", "pass1"),
        ("User171", "somepass"),
        ("User171", "123456789")
    ],
)
def test_wrong_password_field_authorization(
        driver,
        login,
        password,
):
    form = LoginPage(driver)

    form.open()
    form.fill_login_field(login)
    form.fill_password_field(password)
    form.click_login_button()

    notification_text = form.get_notification_text()

    with allure.step("Проверить текст уведомления об ошибке пароля"):
        assert notification_text == INVALID_PASSWORD_MESSAGE, "Неверное сообщение об ошибке пароля"


@allure.label("layer", "UI Tests")
@allure.epic("UI Automation")
@allure.feature("Форма логина")
@allure.story("Неуспешная авторизация")
@allure.title("Отправка формы с некорректным логином и паролем")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.regress
@pytest.mark.parametrize(
    "login, password",
    [
        ("User@", "pass1"),
        ("User$", "somepass"),
        ("User№", "123456789"),
    ],
)
def test_wrong_login_and_password_fields_authorization(
        driver,
        login,
        password,
):
    form = LoginPage(driver)

    form.open()
    form.fill_login_field(login)
    form.fill_password_field(password)
    form.click_login_button()

    notification_text = form.get_notification_text()

    with allure.step("Проверить текст уведомления об ошибках логина и пароля"):
        assert notification_text == INVALID_LOGIN_AND_PASSWORD_MESSAGE, "Неверное сообщение об ошибках логина и пароля"
