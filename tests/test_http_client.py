import pytest
from src.http_client import Client

@pytest.fixture
def http_client():
    return Client()

def test_get(http_client):
    response = http_client.get("test-endpoint")
    assert response is not None

def test_post(http_client):
    response = http_client.post("test-endpoint", data={"key": "value"})
    assert response is not None