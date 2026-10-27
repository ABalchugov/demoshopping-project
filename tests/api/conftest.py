import pytest

from utils import attach


@pytest.fixture
def attach_api():
    return attach.attach_api_response
