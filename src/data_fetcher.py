"""
Data fetcher module for retrieving data from various APIs
"""

from typing import Dict, Any, List, Optional
from src.http_client import HTTPClient
from src.data_processor import DataProcessor


class DataFetcher:
    """
    High-level interface for fetching and processing data from APIs
    """

    def __init__(self, base_url: str = "", timeout: int = 30):
        """
        Initialize the data fetcher

        Args:
            base_url: Base URL for API requests
            timeout: Request timeout in seconds
        """
        self.client = HTTPClient(base_url=base_url, timeout=timeout)
        self.processor = DataProcessor()
        self.cache = {}

    def fetch_user_data(self, user_id: str) -> Dict[str, Any]:
        """
        Fetch user data from API

        Args:
            user_id: User identifier

        Returns:
            User data dictionary
        """
        endpoint = f"users/{user_id}"
        data = self.client.get(endpoint)
        return self.processor.clean_data(data)

    def fetch_posts(self, user_id: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Fetch posts from API, optionally filtered by user

        Args:
            user_id: Optional user ID to filter posts
            limit: Maximum number of posts to fetch

        Returns:
            List of post dictionaries
        """
        params = {'limit': limit}
        if user_id:
            params['userId'] = user_id
        
        endpoint = "posts"
        data = self.client.get(endpoint, params=params)
        
        # Handle both list and dict responses
        if isinstance(data, list):
            return [self.processor.clean_data(post) for post in data]
        elif isinstance(data, dict) and 'posts' in data:
            return [self.processor.clean_data(post) for post in data['posts']]
        else:
            return [self.processor.clean_data(data)]

    def fetch_comments(self, post_id: str) -> List[Dict[str, Any]]:
        """
        Fetch comments for a specific post

        Args:
            post_id: Post identifier

        Returns:
            List of comment dictionaries
        """
        endpoint = f"posts/{post_id}/comments"
        data = self.client.get(endpoint)
        
        if isinstance(data, list):
            return [self.processor.clean_data(comment) for comment in data]
        elif isinstance(data, dict) and 'comments' in data:
            return [self.processor.clean_data(comment) for comment in data['comments']]
        else:
            return [self.processor.clean_data(data)]

    def fetch_analytics(self, resource: str, date_range: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Fetch analytics data for a resource

        Args:
            resource: Resource type (e.g., 'users', 'posts')
            date_range: Optional date range with 'start' and 'end' keys

        Returns:
            Analytics data dictionary
        """
        endpoint = f"analytics/{resource}"
        params = date_range if date_range else {}
        
        data = self.client.get(endpoint, params=params)
        return self.processor.clean_data(data)

    def fetch_with_cache(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Fetch data with caching to avoid duplicate requests

        Args:
            endpoint: API endpoint path
            params: Query parameters

        Returns:
            Cached or freshly fetched data
        """
        cache_key = f"{endpoint}:{str(params)}"
        
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        data = self.client.get(endpoint, params=params)
        cleaned_data = self.processor.clean_data(data)
        self.cache[cache_key] = cleaned_data
        
        return cleaned_data

    def clear_cache(self):
        """Clear the data cache"""
        self.cache.clear()

    def close(self):
        """Close the HTTP client connection"""
        self.client.close()
