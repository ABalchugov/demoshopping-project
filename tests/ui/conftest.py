import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from utils import attach
from utils.config import SELENOID_LOGIN, SELENOID_PASS, SELENOID_URL


@pytest.fixture(scope="function")
def driver(request):
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless").lower() == "true"
    window_size = request.config.getoption("--window_size")
    width_str, height_str = window_size.split("*", 1)

    width = int(width_str) if width_str else 1920
    height = int(height_str) if height_str else 1080

    options = None

    if browser == "chrome":
        options = ChromeOptions()
        options.add_argument(f"--window-size={width},{height}")
    elif browser == "firefox":
        options = FirefoxOptions()
        options.add_argument(f"--width={width}")
        options.add_argument(f"--height={height}")

    if headless:
        options.add_argument("--headless")

    selenoid_url = SELENOID_URL

    if selenoid_url:
        selenoid_capabilities = {
            "browserName": browser,
            "selenoid:options": {
                "enableVNC": True,
                "enableVideo": True
            }
        }
        options.capabilities.update(selenoid_capabilities)
        driver = webdriver.Remote(
            command_executor=(
                f"https://{SELENOID_LOGIN}:{SELENOID_PASS}@{selenoid_url}/wd/hub"
            ),
            options=options
        )
    elif browser == "chrome":
        driver = webdriver.Chrome(options=options)
    else:
        driver = webdriver.Firefox(options=options)

    yield driver

    try:
        attach.add_html(driver)
        attach.add_screenshot(driver)
        attach.add_logs(driver)
        if selenoid_url:
            attach.add_video(driver)
    finally:
        driver.quit()
