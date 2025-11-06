"""
Tests for the api_client module
"""

from unittest.mock import patch, Mock
from src.api_client import (
    fetch_users,
    # fetch_user_posts,
    fetch_comments,
    post_comment,
    check_api_status
)


def mock_requests_get(return_value):
    """Helper to create a mocked GET response"""
    mock_response = Mock()
    mock_response.json.return_value = return_value
    mock_response.raise_for_status.return_value = None
    return mock_response


def test_fetch_users(sample_users):
    """Test fetching all users"""
    with patch('requests.get', return_value=mock_requests_get(sample_users)):
        users = fetch_users()
        assert len(users) == 3
        assert users[0]["name"] == "Alice Johnson"


# def test_fetch_user_posts(sample_posts):
#     """Test fetching posts for a specific user"""
#     user_posts = [p for p in sample_posts if p["user_id"] == "1"]
#     with patch('requests.get', return_value=mock_requests_get(user_posts)):
#         posts = fetch_user_posts("1")
#         assert len(posts) == 2
#         assert all(p["user_id"] == "1" for p in posts)


def test_fetch_comments(sample_comments):
    """Test fetching comments for a post"""
    with patch('requests.get', return_value=mock_requests_get(sample_comments)):
        comments = fetch_comments("1")
        assert len(comments) == 2
        assert comments[0]["content"] == "Great introduction!"


def test_post_comment():
    """Test posting a new comment"""
    expected = {"id": "10", "post_id": "1", "author": "TestUser", "content": "Test comment"}
    
    with patch('requests.post') as mock_post:
        mock_post.return_value = mock_requests_get(expected)
        comment = post_comment("1", "TestUser", "Test comment")
        
        assert comment["post_id"] == "1"
        assert comment["author"] == "TestUser"


def test_check_api_status():
    """Test API status check"""
    with patch('requests.get') as mock_get:
        # Test success
        mock_get.return_value.status_code = 200
        assert check_api_status() is True
        
        # Test failure
        mock_get.side_effect = Exception("Connection failed")
        assert check_api_status() is False
