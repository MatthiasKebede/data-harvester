import pytest
from src.services.user_service import UserService

@pytest.fixture
def user_service():
    return UserService()

def test_fetch_users(user_service):
    users = user_service.fetch_users()
    assert users is not None