import os

from dotenv import load_dotenv


load_dotenv()

TEST_UI_URL = os.getenv("TEST_UI_URL", "").rstrip("/")
SELENOID_URL = os.getenv("SELENOID_URL", "").strip()
SELENOID_LOGIN = os.getenv("SELENOID_LOGIN")
SELENOID_PASS = os.getenv("SELENOID_PASS")
