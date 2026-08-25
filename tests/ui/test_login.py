import pytest
import allure

from pages.login_page import LoginPage


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

    with allure.step("Проверить авторизацию несуществующего пользователя"):
        assert form.non_existed_user_msg_is_displayed() is True, "Удалось авторизовать невалидного пользователя"


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

    msg_is_displayed = form.wrong_login_msg_is_displayed()

    with allure.step("Проверить отображение блока результатов"):
        assert msg_is_displayed is True, "Авторизация прошла с некорректным логином"


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

    msg_is_displayed = form.wrong_password_msg_is_displayed()

    with allure.step("Проверить отображение блока результатов"):
        assert msg_is_displayed is True, "Авторизация прошла с некорректным паролем"


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

    msg_is_displayed = form.wrong_login_and_password_msg_is_displayed()

    with allure.step("Проверить отображение блока результатов"):
        assert msg_is_displayed is True, "Авторизация прошла с некорректными данными"
