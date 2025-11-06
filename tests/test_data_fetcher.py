"""
Tests for data fetcher module
"""

import pytest
from unittest.mock import Mock, patch
from src.data_fetcher import DataFetcher


class TestDataFetcher:
    """Test suite for DataFetcher class"""

    def test_initialization(self):
        """Test data fetcher initialization"""
        fetcher = DataFetcher(base_url="https://api.example.com", timeout=60)
        assert fetcher.client.base_url == "https://api.example.com"
        assert fetcher.client.timeout == 60
        assert fetcher.processor is not None

    @patch('src.data_fetcher.HTTPClient.get')
    def test_fetch_user_data(self, mock_get, sample_user_data):
        """Test fetching user data"""
        mock_get.return_value = sample_user_data
        
        fetcher = DataFetcher(base_url="https://api.example.com")
        result = fetcher.fetch_user_data("123")
        
        assert 'id' in result
        assert 'name' in result
        mock_get.assert_called_once_with("users/123")

    @patch('src.data_fetcher.HTTPClient.get')
    def test_fetch_posts_list_response(self, mock_get, sample_posts_data):
        """Test fetching posts with list response"""
        mock_get.return_value = sample_posts_data
        
        fetcher = DataFetcher(base_url="https://api.example.com")
        result = fetcher.fetch_posts(user_id="123", limit=10)
        
        assert isinstance(result, list)
        assert len(result) == 3
        mock_get.assert_called_once()

    @patch('src.data_fetcher.HTTPClient.get')
    def test_fetch_comments(self, mock_get, sample_comments_data):
        """Test fetching comments for a post"""
        mock_get.return_value = sample_comments_data
        
        fetcher = DataFetcher(base_url="https://api.example.com")
        result = fetcher.fetch_comments("1")
        
        assert isinstance(result, list)
        assert len(result) == 2
        mock_get.assert_called_once_with("posts/1/comments")

    def test_close(self):
        """Test closing the fetcher"""
        fetcher = DataFetcher()
        fetcher.close()
        # No exception should be raised
        assert True
