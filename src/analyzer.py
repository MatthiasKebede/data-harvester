"""
Analyzer module that combines data fetching, processing, and visualization
"""

import matplotlib.pyplot as plt
import matplotlib
import statistics
from typing import Dict, Any, List
from src.api_client import fetch_user, fetch_all_posts

matplotlib.use('Agg')

BASE_URL = "http://localhost:3000"
TIMEOUT = 10


def analyze_user_activity(user_id: str) -> Dict[str, Any]:
    """
    Analyze a user's activity by fetching their posts and creating visualizations
    
    Args:
        user_id: User identifier
        
    Returns:
        Analysis results with stats and plot paths
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
    titles = [p.get("title", f"Post {i}") for i, p in enumerate(posts)]
    
    # Calculate statistics
    analysis = {
        "user_name": user.get("name"),
        "total_posts": len(posts),
        "total_likes": sum(likes),
        "avg_likes": statistics.mean(likes) if likes else 0,
        "total_views": sum(views),
        "avg_views": statistics.mean(views) if views else 0,
    }
    
    # Create bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(range(len(titles)), likes, color='steelblue')
    plt.xlabel('Post Index')
    plt.ylabel('Likes')
    plt.title(f'{user["name"]} - Post Engagement')
    plt.tight_layout()
    likes_plot = f'graphs/user_{user_id}_likes.png'
    plt.savefig(likes_plot)
    plt.close()
    
    # Create line chart
    plt.figure(figsize=(10, 6))
    plt.plot(range(len(views)), views, marker='o', linewidth=2, color='darkgreen')
    plt.xlabel('Post Index')
    plt.ylabel('Views')
    plt.title(f'{user["name"]} - Views Trend')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    views_plot = f'graphs/user_{user_id}_views.png'
    plt.savefig(views_plot)
    plt.close()
    
    analysis['plots'] = [likes_plot, views_plot]
    return analysis


def compare_users(user_ids: List[str]) -> str:
    """
    Compare multiple users' engagement metrics
    
    Args:
        user_ids: List of user identifiers to compare
        
    Returns:
        Path to comparison chart
    """
    # Fetch data
    user_stats = {}
    all_posts = fetch_all_posts()
    
    # Filter posts for each user
    for user_id in user_ids:
        user = fetch_user(user_id)
        posts = [p for p in all_posts if p.get("user_id") == user_id]
        
        likes = [p.get("likes", 0) for p in posts]
        views = [p.get("views", 0) for p in posts]
        user_stats[user["name"]] = {
            "avg_likes": statistics.mean(likes) if likes else 0,
            "avg_views": statistics.mean(views) if views else 0
        }
    
    # Create grouped bar chart
    users = list(user_stats.keys())
    avg_likes = [user_stats[u]["avg_likes"] for u in users]
    avg_views = [user_stats[u]["avg_views"] for u in users]
    
    x = range(len(users))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar([i - width/2 for i in x], avg_likes, width, label='Avg Likes', color='steelblue')
    ax.bar([i + width/2 for i in x], avg_views, width, label='Avg Views', color='coral')
    
    ax.set_xlabel('User')
    ax.set_ylabel('Average Count')
    ax.set_title('User Comparison')
    ax.set_xticks(x)
    ax.set_xticklabels(users)
    ax.legend()
    plt.tight_layout()
    
    plot_path = 'graphs/user_comparison.png'
    plt.savefig(plot_path)
    plt.close()
    
    return plot_path


def analyze_post_distribution() -> Dict[str, Any]:
    """
    Analyze distribution of posts across categories
    
    Returns:
        Distribution analysis with histogram path
    """
    # Fetch data
    posts = fetch_all_posts()
    
    # Count by category
    category_counts = {}
    for post in posts:
        cat = post.get("category", "Uncategorized")
        category_counts[cat] = category_counts.get(cat, 0) + 1
    
    # Create histogram
    plt.figure(figsize=(10, 6))
    plt.bar(category_counts.keys(), category_counts.values(), color='purple', alpha=0.7)
    plt.xlabel('Category')
    plt.ylabel('Number of Posts')
    plt.title('Post Distribution by Category')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    plot_path = 'graphs/category_distribution.png'
    plt.savefig(plot_path)
    plt.close()
    
    return {
        "category_counts": category_counts,
        "plot": plot_path
    }


def analyze_engagement_trends() -> str:
    """
    Analyze engagement trends across all posts
    
    Returns:
        Path to scatter plot
    """
    # Fetch data
    posts = fetch_all_posts()
    views = [p.get("views", 0) for p in posts]
    likes = [p.get("likes", 0) for p in posts]
    
    # Create scatter plot
    plt.figure(figsize=(10, 6))
    plt.scatter(views, likes, alpha=0.6, s=100, color='darkblue')
    plt.xlabel('Views')
    plt.ylabel('Likes')
    plt.title('Engagement: Likes vs Views')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    plot_path = 'graphs/engagement_scatter.png'
    plt.savefig(plot_path)
    plt.close()
    
    return plot_path


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
