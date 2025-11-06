"""
Tests for HTTP client module
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from src.http_client import HTTPClient
import requests


class TestClient:
    """Test suite for HTTPClient class"""

    def test_initialization(self):
        """Test HTTP client initialization"""
        client = HTTPClient(base_url="https://api.example.com", timeout=60)
        assert client.base_url == "https://api.example.com"
        assert client.timeout == 60
        assert client.session is not None

    def test_get_request_success(self, mock_response):
        """Test successful GET request"""
        with patch('requests.Session.get', return_value=mock_response):
            client = HTTPClient(base_url="https://api.example.com")
            result = client.get("users/123")
            assert result == {'success': True}

    def test_post_request_success(self, mock_response):
        """Test successful POST request"""
        with patch('requests.Session.post', return_value=mock_response):
            client = HTTPClient(base_url="https://api.example.com")
            data = {'name': 'Test'}
            result = client.post("users", data=data)
            assert result == {'success': True}

    def test_get_with_params(self):
        """Test GET request with query parameters"""
        mock_resp = Mock()
        mock_resp.json.return_value = {'results': [1, 2, 3]}
        mock_resp.raise_for_status.return_value = None
        
        with patch('requests.Session.get', return_value=mock_resp) as mock_get:
            client = HTTPClient(base_url="https://api.example.com")
            result = client.get("search", params={'q': 'test', 'limit': 10})
            
            assert result == {'results': [1, 2, 3]}
            mock_get.assert_called_once()

    def test_set_auth_token(self):
        """Test setting authentication token"""
        client = HTTPClient()
        client.set_auth_token("test-token-12345")
        assert client.session.headers['Authorization'] == 'Bearer test-token-12345'

    def test_get_multiple_endpoints(self):
        """Test fetching multiple endpoints"""
        mock_resp = Mock()
        mock_resp.json.return_value = {'data': 'test'}
        mock_resp.raise_for_status.return_value = None
        
        with patch('requests.Session.get', return_value=mock_resp):
            client = HTTPClient(base_url="https://api.example.com")
            results = client.get_multiple(['endpoint1', 'endpoint2'])
            
            assert len(results) == 2
            assert all('data' in r for r in results)

    def test_get_request_failure(self):
        """Test GET request with HTTP error"""
        mock_resp = Mock()
        mock_resp.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
        
        with patch('requests.Session.get', return_value=mock_resp):
            client = HTTPClient(base_url="https://api.example.com")
            
            with pytest.raises(requests.exceptions.HTTPError):
                client.get("nonexistent")

    def test_close_session(self):
        """Test closing HTTP session"""
        client = HTTPClient()
        client.close()
        # Verify session is closed (no exception should be raised)
        assert True
