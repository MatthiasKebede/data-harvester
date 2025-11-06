"""
Shared test fixtures and configuration
"""

import pytest
from unittest.mock import Mock


@pytest.fixture
def sample_user_data():
    return {
        'id': '123',
        'name': 'John Doe',
        'email': 'john@example.com',
        'age': 30,
        'city': 'New York'
    }


@pytest.fixture
def sample_posts_data():
    return [
        {'id': '1', 'user_id': '123', 'title': 'First Post', 'views': 100, 'likes': 10},
        {'id': '2', 'user_id': '123', 'title': 'Second Post', 'views': 150, 'likes': 20},
        {'id': '3', 'user_id': '456', 'title': 'Third Post', 'views': 200, 'likes': 30}
    ]


@pytest.fixture
def sample_comments_data():
    return [
        {'id': '1', 'post_id': '1', 'author': 'Alice', 'content': 'Great post!'},
        {'id': '2', 'post_id': '1', 'author': 'Bob', 'content': 'Thanks for sharing'}
    ]


@pytest.fixture
def mock_response():
    """Create a mock response object"""
    mock = Mock()
    mock.status_code = 200
    mock.json.return_value = {'success': True}
    mock.raise_for_status.return_value = None
    return mock
