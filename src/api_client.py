"""
API client module for fetching data from APIs
"""

import requests
from typing import Dict, Any, List

BASE_URL = "http://localhost:3000"
TIMEOUT = 10


def fetch_users() -> List[Dict[str, Any]]:
    """
    Fetch all users from the API
    
    Returns:
        List of user dictionaries
    """
    response = requests.get(f"{BASE_URL}/users", timeout=TIMEOUT)
    response.raise_for_status()
    return response.json()


def fetch_user(user_id: str) -> Dict[str, Any]:
    """
    Fetch a single user by ID
    
    Args:
        user_id: User identifier
        
    Returns:
        User data dictionary
    """
    response = requests.get(f"{BASE_URL}/users/{user_id}", timeout=TIMEOUT)
    response.raise_for_status()
    return response.json()


# def fetch_user_posts(user_id: str) -> List[Dict[str, Any]]:
#     """
#     Fetch all posts for a specific user
    
#     Args:
#         user_id: User identifier
        
#     Returns:
#         List of post dictionaries
#     """
#     response = requests.get(
#         f"{BASE_URL}/posts",
#         params={"user_id": user_id},
#         timeout=TIMEOUT
#     )
#     response.raise_for_status()
#     return response.json()


def fetch_posts_by_category(category: str) -> List[Dict[str, Any]]:
    """
    Fetch posts filtered by category
    
    Args:
        category: Category name to filter by
        
    Returns:
        List of post dictionaries in the category
    """
    response = requests.get(
        f"{BASE_URL}/posts",
        params={"category": category},
        timeout=TIMEOUT
    )
    response.raise_for_status()
    return response.json()


def fetch_all_posts() -> List[Dict[str, Any]]:
    """
    Fetch all posts from the API
    
    Returns:
        List of all post dictionaries
    """
    response = requests.get(f"{BASE_URL}/posts", timeout=TIMEOUT)
    response.raise_for_status()
    return response.json()


def fetch_post(post_id: str) -> Dict[str, Any]:
    """
    Fetch a single post by ID
    
    Args:
        post_id: Post identifier
        
    Returns:
        Post data dictionary
    """
    response = requests.get(f"{BASE_URL}/posts/{post_id}", timeout=TIMEOUT)
    response.raise_for_status()
    return response.json()


def fetch_comments(post_id: str) -> List[Dict[str, Any]]:
    """
    Fetch comments for a specific post
    
    Args:
        post_id: Post identifier
        
    Returns:
        List of comment dictionaries
    """
    response = requests.get(
        f"{BASE_URL}/posts/{post_id}/comments",
        timeout=TIMEOUT
    )
    response.raise_for_status()
    return response.json()


def post_comment(post_id: str, author: str, content: str) -> Dict[str, Any]:
    """
    Post a new comment to a post
    
    Args:
        post_id: Post identifier
        author: Comment author name
        content: Comment content
        
    Returns:
        Created comment data
    """
    comment_data = {
        "post_id": post_id,
        "author": author,
        "content": content
    }
    
    response = requests.post(
        f"{BASE_URL}/comments",
        json=comment_data,
        headers={"Content-Type": "application/json"},
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
