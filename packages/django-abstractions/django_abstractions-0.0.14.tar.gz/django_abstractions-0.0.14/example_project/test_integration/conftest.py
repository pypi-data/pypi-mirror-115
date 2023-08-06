import pytest
from django.test import Client


@pytest.fixture(
    autouse=True
)
def client():
    return Client()
