from uuid import uuid4

import allure
import pytest

from pages.registration_page import RegistrationPage


INVALID_LOGIN_MESSAGE = (
    "Логин должен содержать от 3 до 15 символов и может включать буквы, цифры и символы: _"
)
INVALID_PASSWORD_MESSAGE = (
    "Пароль должен содержать не менее 8 символов, включая минимум одну букву и одну цифру"
)
INVALID_LOGIN_AND_PASSWORD_MESSAGE = f"{INVALID_LOGIN_MESSAGE} {INVALID_PASSWORD_MESSAGE}"
REGISTRATION_SUCCESS_MESSAGE = "Регистрация выполнена успешно"


@allure.label("layer", "UI Tests")
@allure.epic("UI Automation")
@allure.feature("Форма регистрации")
@allure.story("Успешная регистрация")
@allure.title("Отправка формы с корректными данными")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.regress
@pytest.mark.parametrize(
    "login, password",
    [
        (f"User{uuid4().hex[:11]}", "somepass1"),
    ],
)
def test_positive_registration(
        driver,
        login,
        password,
):
    form = RegistrationPage(driver)

    form.open()
    form.fill_login_field(login)
    form.fill_password_field(password)
    form.click_registration_button()

    notification_text = form.get_notification_text()

    with allure.step("Проверить текст уведомления об успешной регистрации"):
        assert notification_text == REGISTRATION_SUCCESS_MESSAGE, "Неверное сообщение об успешной регистрации"


@allure.label("layer", "UI Tests")
@allure.epic("UI Automation")
@allure.feature("Форма регистрации")
@allure.story("Неуспешная регистрация")
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
def test_wrong_login_field_registration(
        driver,
        login,
        password,
):
    form = RegistrationPage(driver)

    form.open()
    form.fill_login_field(login)
    form.fill_password_field(password)
    form.click_registration_button()

    notification_text = form.get_notification_text()

    with allure.step("Проверить текст уведомления об ошибке логина"):
        assert notification_text == INVALID_LOGIN_MESSAGE, "Неверное сообщение об ошибке логина"


@allure.label("layer", "UI Tests")
@allure.epic("UI Automation")
@allure.feature("Форма регистрации")
@allure.story("Неуспешная регистрация")
@allure.title("Отправка формы с некорректным паролем")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.regress
@pytest.mark.parametrize(
    "login, password",
    [
        (f"User{uuid4().hex[:11]}", "pass1"),
        (f"User{uuid4().hex[:11]}", "somepass"),
        (f"User{uuid4().hex[:11]}", "123456789")
    ],
)
def test_wrong_password_field_registration(
        driver,
        login,
        password,
):
    form = RegistrationPage(driver)

    form.open()
    form.fill_login_field(login)
    form.fill_password_field(password)
    form.click_registration_button()

    notification_text = form.get_notification_text()

    with allure.step("Проверить текст уведомления об ошибке пароля"):
        assert notification_text == INVALID_PASSWORD_MESSAGE, "Неверное сообщение об ошибке пароля"


@allure.label("layer", "UI Tests")
@allure.epic("UI Automation")
@allure.feature("Форма регистрации")
@allure.story("Неуспешная регистрация")
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
def test_wrong_login_and_password_fields_registration(
        driver,
        login,
        password,
):
    form = RegistrationPage(driver)

    form.open()
    form.fill_login_field(login)
    form.fill_password_field(password)
    form.click_registration_button()

    notification_text = form.get_notification_text()

    with allure.step("Проверить текст уведомления об ошибках логина и пароля"):
        assert notification_text == INVALID_LOGIN_AND_PASSWORD_MESSAGE, "Неверное сообщение об ошибках логина и пароля"
