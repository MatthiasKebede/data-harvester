"""
Analyzer module that combines data fetching, processing, and storage
"""

import tablib
import os
import statistics
from typing import Dict, Any, List
from src.api_client import fetch_user, fetch_all_posts


def analyze_user_activity(user_id: str) -> Dict[str, Any]:
    """
    Analyze a user's activity by fetching their posts and saving the results
    
    Args:
        user_id: User identifier
        
    Returns:
        Analysis results with stats and CSV export path
    """
    # Fetch data
    user = fetch_user(user_id)
    all_posts = fetch_all_posts()
    posts = [p for p in all_posts if p.get("user_id") == user_id]
    if not posts:
        return {"error": "No posts found"}
    
    # Extract metrics
    likes = [p.get("likes", 0) for p in posts]
    views = [p.get("views", 0) for p in posts]
    
    # Calculate statistics
    analysis = {
        "user": user.get("name"),
        "total_posts": len(posts),
        "total_likes": sum(likes),
        "avg_likes": statistics.mean(likes) if likes else 0,
        "total_views": sum(views),
        "avg_views": statistics.mean(views) if views else 0,
    }
    
    # Create data for export
    dataset = tablib.Dataset()
    dataset.headers = ['post_index', 'title', 'likes', 'views', 'category']
    
    for i, post in enumerate(posts):
        dataset.append([
            i,
            post.get('title', f'Post {i}'),
            post.get('likes', 0),
            post.get('views', 0),
            post.get('category', 'Uncategorized')
        ])
    
    # Sort by likes (descending)
    dataset = dataset.sort('likes', reverse=True)

    # Export CSV file
    csv_output = dataset.export('csv')
    csv_path = f'data/user_{user_id}_posts.csv'
    os.makedirs('data', exist_ok=True)
    with open(csv_path, 'w', encoding='utf-8') as csvfile:
        csvfile.write(csv_output)
    
    analysis['path'] = csv_path
    return analysis


def analyze_engagement_trends() -> str:
    """
    Analyze engagement trends across all posts
    
    Returns:
        Path to engagement data CSV file
    """
    # Fetch data
    posts = fetch_all_posts()
    
    # Create data for export
    dataset = tablib.Dataset()
    dataset.headers = ['post_id', 'title', 'views', 'likes', 'engagement_ratio']
    
    for post in posts:
        views = post.get("views", 0)
        likes = post.get("likes", 0)
        engagement_ratio = likes / views if views > 0 else 0
        
        dataset.append([
            post.get('id', ''),
            post.get('title', 'Untitled'),
            views,
            likes,
            round(engagement_ratio, 4)
        ])
    
    # Export CSV file
    csv_path = 'data/engagement_trends.csv'
    os.makedirs('data', exist_ok=True)
    with open(csv_path, 'w', encoding='utf-8') as csvfile:
        csvfile.write(dataset.export('csv'))
    
    return csv_path


def calculate_average_title_length(posts: List[Dict[str, Any]]) -> float:
    """
    Calculate the average character length of post titles
    
    Args:
        posts: List of post dictionaries containing 'title' field
        
    Returns:
        Average title length as a float, or 0.0 if no posts provided
    """
    # TODO: Implement this function
    pass
