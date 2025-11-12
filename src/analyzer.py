"""
Analyzer module that combines data fetching, processing, and storage
"""

import csv
import os
import statistics
from typing import Dict, Any, List
from src.api_client import fetch_user, fetch_all_posts


BASE_URL = "http://localhost:3000"
TIMEOUT = 10


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
    
    # Export detailed post data to CSV
    csv_path = f'data/user_{user_id}_posts.csv'
    os.makedirs('data', exist_ok=True)
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['post_index', 'title', 'likes', 'views', 'category']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for i, post in enumerate(posts):
            writer.writerow({
                'post_index': i,
                'title': post.get('title', f'Post {i}'),
                'likes': post.get('likes', 0),
                'views': post.get('views', 0),
                'category': post.get('category', 'Uncategorized')
            })
    
    analysis['path'] = csv_path
    return analysis


def analyze_post_distribution() -> Dict[str, Any]:
    """
    Analyze distribution of posts across categories
    
    Returns:
        Distribution analysis with CSV file path
    """
    # Fetch data
    posts = fetch_all_posts()
    
    # Count by category
    category_counts = {}
    for post in posts:
        cat = post.get("category", "Uncategorized")
        category_counts[cat] = category_counts.get(cat, 0) + 1
    
    # Export distribution data to CSV
    csv_path = 'data/category_distribution.csv'
    os.makedirs('data', exist_ok=True)
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['category', 'post_count']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for category, count in category_counts.items():
            writer.writerow({
                'category': category,
                'post_count': count
            })
    
    return {
        "category_counts": category_counts,
        "path": csv_path
    }


def analyze_engagement_trends() -> str:
    """
    Analyze engagement trends across all posts
    
    Returns:
        Path to engagement data CSV file
    """
    # Fetch data
    posts = fetch_all_posts()
    
    # Export engagement data to CSV
    csv_path = 'data/engagement_trends.csv'
    os.makedirs('data', exist_ok=True)
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['post_id', 'title', 'views', 'likes', 'engagement_ratio']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for post in posts:
            views = post.get("views", 0)
            likes = post.get("likes", 0)
            engagement_ratio = likes / views if views > 0 else 0
            
            writer.writerow({
                'post_id': post.get('id', ''),
                'title': post.get('title', 'Untitled'),
                'views': views,
                'likes': likes,
                'engagement_ratio': round(engagement_ratio, 4)
            })
    
    return csv_path


def calculate_average_post_length(posts: List[Dict[str, Any]]) -> float:
    """
    Calculate the average character length of post titles
    
    Args:
        posts: List of post dictionaries containing 'title' field
        
    Returns:
        Average title length as a float, or 0.0 if no posts provided
    """
    # TODO: Implement this function
    pass
