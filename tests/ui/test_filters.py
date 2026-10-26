import allure
import pytest

from pages.catalog_page import CatalogPage
from pages.filter_page import FilterPage


@allure.label("layer", "UI Tests")
@allure.epic("UI Automation")
@allure.feature("Каталог")
@allure.story("Фильтры")
@allure.title("Проверка фильтра Мин. цена")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.smoke
@pytest.mark.regress
@pytest.mark.parametrize(
    "price",
    [
        1000,
        1477,
        1,
        -1,
        0,
        999999
    ],
)
def test_min_price_filter(driver, price):
    form = FilterPage(driver)
    catalog = CatalogPage(driver)

    form.open()
    catalog.wait_for_catalog_loaded()

    form.fill_min_price_filter(price)
    previous_cards = catalog.get_cards()
    form.click_apply_filters_button()
    catalog.wait_for_catalog_updated(previous_cards)

    first_card = catalog.get_first_card()
    params = catalog.get_card_parameters(first_card)

    if params:
        assert params["price"] >= price, (
            f"Цена {params['price']} меньше минимальной цены {price}"
        )
    else:
        allure.attach("Список пуст — нет товаров с ценой ниже заданной", name="Инфо")


@allure.label("layer", "UI Tests")
@allure.epic("UI Automation")
@allure.feature("Каталог")
@allure.story("Фильтры")
@allure.title("Проверка фильтра Макс. цена")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.smoke
@pytest.mark.regress
@pytest.mark.parametrize(
    "price",
    [
        1000,
        1477,
        1,
        -1,
        0,
        999999
    ],
)
def test_max_price_filter(
        driver, price
):
    form = FilterPage(driver)
    catalog = CatalogPage(driver)

    form.open()
    catalog.wait_for_catalog_loaded()

    form.fill_max_price_filter(price)
    previous_cards = catalog.get_cards()
    form.click_apply_filters_button()
    catalog.wait_for_catalog_updated(previous_cards)

    first_card = catalog.get_first_card()
    params = catalog.get_card_parameters(first_card)

    if params:
        assert params["price"] <= price, (
            f"Цена {params['price']} больше максимальной цены {price}"
        )
    else:
        allure.attach("Список пуст — нет товаров с ценой выше заданной", name="Инфо")


@allure.label("layer", "UI Tests")
@allure.epic("UI Automation")
@allure.feature("Каталог")
@allure.story("Фильтры")
@allure.title("Проверка фильтра категории")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.smoke
@pytest.mark.regress
@pytest.mark.parametrize(
    "category",
    [
        "",
        "Laptops",
        "Phones",
        "Watches",
    ],
)
def test_category_filter(
        driver, category
):
    form = FilterPage(driver)
    catalog = CatalogPage(driver)

    form.open()
    catalog.wait_for_catalog_loaded()

    form.choose_categories_filter(category)
    previous_cards = catalog.get_cards()
    form.click_apply_filters_button()
    catalog.wait_for_catalog_updated(previous_cards)

    first_card = catalog.get_first_card()
    params = catalog.get_card_parameters(first_card)

    assert params, "Список карточек пуст после применения фильтра"

    if category:
        assert params["category"] == category, "Категория в карточке не соответствует фильтру"


@allure.label("layer", "UI Tests")
@allure.epic("UI Automation")
@allure.feature("Каталог")
@allure.story("Фильтры")
@allure.title("Проверка фильтра производитель")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.smoke
@pytest.mark.regress
@pytest.mark.parametrize(
    "manufacturer",
    [
        "",
        "Apple",
        "Xiaomi",
        "Huawei",
        "Samsung"
    ],
)
def test_manufacturer_filter(
        driver, manufacturer
):
    form = FilterPage(driver)
    catalog = CatalogPage(driver)

    form.open()
    catalog.wait_for_catalog_loaded()

    form.choose_manufacturer_filter(manufacturer)
    previous_cards = catalog.get_cards()
    form.click_apply_filters_button()
    catalog.wait_for_catalog_updated(previous_cards)

    first_card = catalog.get_first_card()
    params = catalog.get_card_parameters(first_card)

    assert params, "Список карточек пуст после применения фильтра"

    if manufacturer:
        assert params["manufacturer"] == manufacturer, "Производитель в карточке не соответствует фильтру"


@allure.label("layer", "UI Tests")
@allure.epic("UI Automation")
@allure.feature("Каталог")
@allure.story("Фильтры")
@allure.title("Проверка чекбокса бесплатная доставка")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.smoke
@pytest.mark.regress
def test_free_shipping_checkbox_filter(driver):
    form = FilterPage(driver)
    catalog = CatalogPage(driver)

    form.open()
    catalog.wait_for_catalog_loaded()

    form.click_free_shipping_checkbox_filter()
    previous_cards = catalog.get_cards()
    form.click_apply_filters_button()
    catalog.wait_for_catalog_updated(previous_cards)

    first_card = catalog.get_first_card()
    params = catalog.get_card_parameters(first_card)

    assert params, "Список карточек пуст после применения фильтра"
    assert params["free_shipping"] == "Да", "Карточка не соответствует фильтру бесплатная доставка"


@allure.label("layer", "UI Tests")
@allure.epic("UI Automation")
@allure.feature("Каталог")
@allure.story("Фильтры")
@allure.title("Проверка кнопки сброса")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.smoke
@pytest.mark.regress
@pytest.mark.parametrize("max_price", [1000, -1])
def test_reset_filters_button(driver, max_price):
    form = FilterPage(driver)
    catalog = CatalogPage(driver)

    form.open()
    catalog.wait_for_catalog_loaded()
    initial_catalog = [card.text for card in catalog.get_cards()]

    form.fill_min_price_filter(1)
    form.fill_max_price_filter(max_price)
    form.choose_categories_filter("Phones")
    form.choose_manufacturer_filter("Apple")
    form.click_free_shipping_checkbox_filter()

    cards_before_apply = catalog.get_cards()
    form.click_apply_filters_button()
    catalog.wait_for_catalog_updated(cards_before_apply)

    cards_before_reset = catalog.get_cards()
    form.click_reset_filters_button()
    if cards_before_reset:
        catalog.wait_for_catalog_updated(cards_before_reset)
    else:
        catalog.wait_for_catalog_loaded()

    restored_catalog = [card.text for card in catalog.get_cards()]
    assert restored_catalog == initial_catalog, "Каталог не восстановился после сброса фильтров"

    new_state = form.get_filters_state()

    assert new_state.min_price == "", "Поле Мин цена не очистилось"
    assert new_state.max_price == "", "Поле Макс цена не очистилось"
    assert new_state.category == "", "Поле Категория не очистилось"
    assert new_state.manufacturer == "", "Поле Производитель не очистилось"
    assert not new_state.free_shipping, "Чекбокс Бесплатная доставка не сбросился"
