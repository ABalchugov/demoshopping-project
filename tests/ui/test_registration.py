import random

import pytest
import allure

from pages.registration_page import RegistrationPage


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
        (f"User{random.randint(1, 1000)}", "somepass1"),
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

    msg_is_displayed = form.success_registration_msg_is_displayed()

    with allure.step("Проверить отображение блока результатов"):
        assert msg_is_displayed is True, "Регистрация не успешна"


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

    msg_is_displayed = form.wrong_login_msg_is_displayed()

    with allure.step("Проверить отображение блока результатов"):
        assert msg_is_displayed is True, "Регистрация прошла с некорректным логином"


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
        (f"User{random.randint(1, 1000)}", "pass1"),
        (f"User{random.randint(1, 1000)}", "somepass"),
        (f"User{random.randint(1, 1000)}", "123456789")
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

    msg_is_displayed = form.wrong_password_msg_is_displayed()

    with allure.step("Проверить отображение блока результатов"):
        assert msg_is_displayed is True, "Регистрация прошла с некорректным паролем"


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

    msg_is_displayed = form.wrong_login_and_password_msg_is_displayed()

    with allure.step("Проверить отображение блока результатов"):
        assert msg_is_displayed is True, "Регистрация прошла с некорректными данными"
