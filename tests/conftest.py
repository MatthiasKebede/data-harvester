"""
Shared test fixtures and configuration
"""

import pytest


@pytest.fixture(scope="session")
def sample_users():
    """Sample list of users for testing"""
    return [
        {'id': '1', 'name': 'Alice Johnson', 'email': 'alice@example.com'},
        {'id': '2', 'name': 'Bob Smith', 'email': 'bob@example.com'},
        {'id': '3', 'name': 'Carol White', 'email': 'carol@example.com'}
    ]


@pytest.fixture(scope="session")
def sample_user(sample_users):
    """Sample user data for testing"""
    return sample_users[0]


@pytest.fixture(scope="session")
def sample_posts():
    """Sample posts data for testing"""
    return [
        {'id': '1', 'user_id': '1', 'title': 'Getting Started with Python', 'likes': 45, 'views': 230, 'category': 'Technology'},
        {'id': '2', 'user_id': '1', 'title': 'Data Science Tips', 'likes': 67, 'views': 312, 'category': 'Technology'},
        {'id': '3', 'user_id': '2', 'title': 'Healthy Living', 'likes': 34, 'views': 189, 'category': 'Health'},
        {'id': '4', 'user_id': '2', 'title': 'Exercise Routines', 'likes': 52, 'views': 276, 'category': 'Health'},
        {'id': '5', 'user_id': '3', 'title': 'Learning Strategies', 'likes': 41, 'views': 198, 'category': 'Education'}
    ]


@pytest.fixture(scope="session")
def sample_post(sample_posts):
    """Sample single post for testing"""
    return sample_posts[0]


@pytest.fixture(scope="session")
def sample_comments():
    """Sample comments data for testing"""
    return [
        {'id': '1', 'post_id': '1', 'author': 'Mike', 'content': 'Great introduction!'},
        {'id': '2', 'post_id': '1', 'author': 'Sarah', 'content': 'Very helpful, thanks!'}
    ]
