"""
HTTP Client module for making API requests
"""

import requests
from typing import Dict, Any, Optional, List
import json


class HTTPClient:
    """
    A client for making HTTP requests to APIs. Handles GET and POST requests with error handling.
    """

    def __init__(self, base_url: str = "", timeout: int = 30):
        """
        Initialize the HTTP client

        Args:
            base_url: Base URL for API requests
            timeout: Request timeout in seconds
        """
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'DataHarvester/1.0',
            'Accept': 'application/json'
        })

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make a GET request to the specified endpoint

        Args:
            endpoint: API endpoint path
            params: Query parameters

        Returns:
            JSON response as dictionary

        Raises:
            requests.exceptions.RequestException: If request fails
        """
        url = self._build_url(endpoint)
        response = self.session.get(url, params=params, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make a POST request to the specified endpoint

        Args:
            endpoint: API endpoint path
            data: Request body data

        Returns:
            JSON response as dictionary

        Raises:
            requests.exceptions.RequestException: If request fails
        """
        url = self._build_url(endpoint)
        response = self.session.post(url, json=data, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def get_multiple(self, endpoints: List[str]) -> List[Dict[str, Any]]:
        """
        Make multiple GET requests to different endpoints

        Args:
            endpoints: List of API endpoint paths

        Returns:
            List of JSON responses
        """
        results = []
        for endpoint in endpoints:
            try:
                result = self.get(endpoint)
                results.append(result)
            except requests.exceptions.RequestException as e:
                results.append({"error": str(e), "endpoint": endpoint})
        return results

    def _build_url(self, endpoint: str) -> str:
        """
        Build full URL from base URL and endpoint

        Args:
            endpoint: API endpoint path

        Returns:
            Complete URL
        """
        if self.base_url:
            return f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        return endpoint

    def set_auth_token(self, token: str):
        """
        Set authentication token in session headers

        Args:
            token: Bearer token for authentication
        """
        self.session.headers.update({'Authorization': f'Bearer {token}'})

    def close(self):
        """Close the HTTP session"""
        self.session.close()
