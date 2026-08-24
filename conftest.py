import os

import pytest
from selenium import webdriver
from dotenv import load_dotenv

@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv()

@pytest.fixture(scope="function", autouse=True)
def driver():
    print("\n\n>>> Открываем браузер <<<")
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver

    print("\n\n>>> Закрываем браузер <<<")
    driver.quit()