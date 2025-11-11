"""
API client module for fetching data from APIs
"""

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import json
from typing import Dict, Any, List, Iterator

BASE_URL = "http://localhost:3000"
TIMEOUT = 3

_session = None

def get_session() -> requests.Session:
    """Get or create a shared session"""
    global _session
    if _session is None:
        adapter = HTTPAdapter(pool_connections=10, pool_maxsize=20)
        _session = requests.Session()
        _session.mount("http://", adapter)
        _session.mount("https://", adapter)
    return _session


def fetch_all_users() -> List[Dict[str, Any]]:
    """
    Fetch all users, with session
    
    Returns:
        List of user dictionaries
    """
    session = get_session()
    response = session.get(f"{BASE_URL}/users")
    response.raise_for_status()
    return response.json()


def fetch_user(user_id: str) -> Dict[str, Any]:
    """
    Fetch a single user by ID, with retry session
    
    Args:
        user_id: User identifier
        
    Returns:
        User data dictionary
    """
    session = requests.Session()
    retry_strategy = Retry(total=1, backoff_factor=1)
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    try:
        response = session.get(f"{BASE_URL}/users/{user_id}", timeout=TIMEOUT)
        response.raise_for_status()
        return response.json()
    finally:
        session.close()


def fetch_all_posts() -> List[Dict[str, Any]]:
    """
    Fetch all posts from the API, with custom headers
    
    Returns:
        List of all post dictionaries
    """
    response = requests.get(
        f"{BASE_URL}/posts",
        headers = {
            "Accept": "application/json",
            "User-Agent": "DataHarvester/1.0"
        },
        timeout=TIMEOUT
    )
    response.raise_for_status()
    return response.json()


def fetch_comments(post_id: str) -> Iterator[Dict[str, Any]]:
    """
    Fetch comments for a specific post, with streaming
    
    Args:
        post_id: Post identifier
        
    Returns:
        List of comment dictionaries
    """
    response = requests.get(f"{BASE_URL}/posts/{post_id}/comments", stream=True)
    response.raise_for_status()

    # Accumulate chunks
    chunks = []
    for chunk in response.iter_content(chunk_size=512):
        if chunk:
            chunks.append(chunk)

    # Parse complete response and yield individual comments
    content = b''.join(chunks).decode('utf-8')
    comments = json.loads(content)
    for comment in comments:
        yield comment


def post_comment(post_id: str, author: str, content: str) -> Dict[str, Any]:
    """
    Post a new comment to a post, with encoding
    
    Args:
        post_id: Post identifier
        author: Comment author name
        content: Comment content
        
    Returns:
        Created comment data
    """
    response = requests.post(
        f"{BASE_URL}/comments",
        json={"post_id": post_id, "author": author, "content": content},
        headers={"Content-Type": "application/json; charset=utf-8"},
        timeout=TIMEOUT
    )
    response.raise_for_status()
    return response.json()


def check_api_status() -> bool:
    """
    Check if the API is responding
    
    Returns:
        True if API is healthy, False otherwise
    """
    try:
        response = requests.get(f"{BASE_URL}/users", timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def close_session():
    """Close and clean up global session"""
    global _session
    if _session is not None:
        _session.close()
        _session = None
