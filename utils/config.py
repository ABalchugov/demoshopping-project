import os

from dotenv import load_dotenv

load_dotenv()

TEST_UI_URL = os.getenv("TEST_UI_URL", "").rstrip("/")
TEST_API_URL = os.getenv("TEST_API_URL", "").rstrip("/")
API_USERNAME = os.getenv("API_USERNAME", "")
API_PASSWORD = os.getenv("API_PASSWORD", "")
API_REGISTRATION_USERNAME = os.getenv("API_REGISTRATION_USERNAME", "")
API_REGISTRATION_PASSWORD = os.getenv("API_REGISTRATION_PASSWORD", "")
UI_USERNAME = os.getenv("UI_USERNAME", "")
UI_PASSWORD = os.getenv("UI_PASSWORD", "")
SELENOID_URL = os.getenv("SELENOID_URL", "").strip()
SELENOID_LOGIN = os.getenv("SELENOID_LOGIN")
SELENOID_PASS = os.getenv("SELENOID_PASS")
