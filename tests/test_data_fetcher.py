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
    def test_fetch_posts_dict_response(self, mock_get, sample_posts_data):
        """Test fetching posts with dict response"""
        mock_get.return_value = {'posts': sample_posts_data}
        
        fetcher = DataFetcher(base_url="https://api.example.com")
        result = fetcher.fetch_posts(limit=5)
        
        assert isinstance(result, list)
        assert len(result) == 3

    @patch('src.data_fetcher.HTTPClient.get')
    def test_fetch_comments(self, mock_get, sample_comments_data):
        """Test fetching comments for a post"""
        mock_get.return_value = sample_comments_data
        
        fetcher = DataFetcher(base_url="https://api.example.com")
        result = fetcher.fetch_comments("1")
        
        assert isinstance(result, list)
        assert len(result) == 2
        mock_get.assert_called_once_with("posts/1/comments")

    @patch('src.data_fetcher.HTTPClient.get')
    def test_fetch_analytics(self, mock_get, sample_analytics_data):
        """Test fetching analytics data"""
        mock_get.return_value = sample_analytics_data
        
        fetcher = DataFetcher(base_url="https://api.example.com")
        result = fetcher.fetch_analytics("posts", date_range={'start': '2025-01-01', 'end': '2025-11-05'})
        
        assert 'resource' in result
        assert 'total_views' in result
        mock_get.assert_called_once()

    @patch('src.data_fetcher.HTTPClient.get')
    def test_fetch_with_cache(self, mock_get):
        """Test caching functionality"""
        mock_get.return_value = {'data': 'cached'}
        
        fetcher = DataFetcher(base_url="https://api.example.com")
        
        # First call - should hit the API
        result1 = fetcher.fetch_with_cache("test", params={'key': 'value'})
        assert result1 == {'data': 'cached'}
        
        # Second call with same params - should use cache
        result2 = fetcher.fetch_with_cache("test", params={'key': 'value'})
        assert result2 == {'data': 'cached'}
        
        # Should only call the API once
        assert mock_get.call_count == 1

    def test_clear_cache(self):
        """Test clearing the cache"""
        fetcher = DataFetcher()
        fetcher.cache = {'key1': 'value1', 'key2': 'value2'}
        
        fetcher.clear_cache()
        assert len(fetcher.cache) == 0

    def test_close(self):
        """Test closing the fetcher"""
        fetcher = DataFetcher()
        fetcher.close()
        # No exception should be raised
        assert True
