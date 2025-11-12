"""
Tests for the api_client module
"""

import httpx
import json
from unittest.mock import patch, Mock, MagicMock
from src.api_client import (
    fetch_all_users,
    fetch_comments,
    post_comment,
    check_api_status
)


def mock_response(return_value, status_code=200):
    """Helper to create a mocked GET response"""
    mock_resp = Mock()
    mock_resp.json.return_value = return_value
    mock_resp.status_code = status_code
    mock_resp.raise_for_status.return_value = None
    mock_resp.text = str(return_value)
    return mock_resp


def test_fetch_users(sample_users):
    """Test fetching all users"""
    with patch('src.api_client.get_session') as mock_get_session:
        mock_session = MagicMock()
        mock_session.get.return_value = mock_response(sample_users)
        mock_get_session.return_value = mock_session

        users = fetch_all_users()
        assert len(users) == 3
        assert users[0]["name"] == "Alice Johnson"


def test_fetch_comments(sample_comments):
    """Test fetching comments for a post"""
    with patch('httpx.stream') as mock_get:
        # Mock streaming response
        mock_resp = Mock()
        mock_resp.raise_for_status.return_value = None
        content_bytes = json.dumps(sample_comments).encode('utf-8')
        mock_resp.iter_bytes.return_value = iter([content_bytes])
        mock_get.return_value = mock_resp

        comments = list(fetch_comments("1"))
        assert len(comments) == 2
        assert comments[0]["content"] == "Great introduction!"


def test_post_comment():
    """Test posting a new comment"""
    expected = {"id": "10", "post_id": "1", "author": "TestUser", "content": "Test comment"}
    
    with patch('httpx.post') as mock_post:
        mock_post.return_value = mock_response(expected)

        comment = post_comment("1", "TestUser", "Test comment")
        assert comment["post_id"] == "1"
        assert comment["author"] == "TestUser"
        assert comment["content"] == "Test comment"


def test_check_api_status():
    """Test API status check"""
    with patch('httpx.get') as mock_get:
        # Test success
        mock_get.return_value.status_code = 200
        assert check_api_status() is True
        
        # Test failure
        mock_get.side_effect = httpx._exceptions.RequestError("Connection failed")
        assert check_api_status() is False
