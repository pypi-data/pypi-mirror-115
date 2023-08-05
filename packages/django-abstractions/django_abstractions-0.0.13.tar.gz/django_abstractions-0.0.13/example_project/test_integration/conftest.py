import pytest
from django.test import Client


@pytest.fixture
def client():
    return Client()


# @pytest.fixture(autouse=True)
# def test_settings(settings):
#     settings.TESTING_MODE = True
#     return settings
