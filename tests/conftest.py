import pytest
from src.http_client import Client

@pytest.fixture
def http_client():
    return Client()