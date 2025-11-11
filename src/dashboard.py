"""
Dashboard module for generating comprehensive reports and visualizations
"""

import matplotlib.pyplot as plt
import matplotlib
from typing import Dict, Any
import json
import os
from src.api_client import fetch_user, fetch_all_users, fetch_all_posts

matplotlib.use('Agg')

BASE_URL = "http://localhost:3000"
TIMEOUT = 10


def generate_overview_dashboard() -> Dict[str, Any]:
    """
    Generate a dashboard with overview statistics and visualizations
    
    Returns:
        Dashboard data with plot paths
    """
    # Fetch data
    users = fetch_all_users()
    posts = fetch_all_posts()
    
    # Calculate metrics
    dashboard = {
        "total_users": len(users),
        "total_posts": len(posts),
        "avg_posts_per_user": len(posts) / len(users) if users else 0
    }
    
    # Create overview bar chart
    metrics = ['Users', 'Posts', 'Avg Posts/User']
    values = [dashboard["total_users"], dashboard["total_posts"], dashboard["avg_posts_per_user"]]
    
    plt.figure(figsize=(10, 6))
    plt.bar(metrics, values, color=['steelblue', 'coral', 'lightgreen'])
    plt.ylabel('Count')
    plt.title('Platform Overview')
    plt.tight_layout()
    
    overview_plot = 'reports/figures/overview.png'
    os.makedirs('reports/figures', exist_ok=True)
    plt.savefig(overview_plot)
    plt.close()
    
    dashboard['overview_plot'] = overview_plot
    
    # Count posts per user
    user_post_counts = {}
    for post in posts:
        uid = post.get("user_id", "unknown")
        user_post_counts[uid] = user_post_counts.get(uid, 0) + 1
    
    # Create pie chart
    plt.figure(figsize=(8, 8))
    plt.pie(
        user_post_counts.values(),
        labels=[f"User {uid}" for uid in user_post_counts.keys()],
        autopct='%1.1f%%',
        startangle=90
    )
    plt.title('Post Distribution by User')
    
    pie_plot = 'reports/figures/posts_distribution.png'
    plt.savefig(pie_plot)
    plt.close()
    
    dashboard['pie_plot'] = pie_plot
    
    return dashboard


def generate_user_report(user_id: str) -> Dict[str, Any]:
    """
    Generate detailed report for a specific user
    
    Args:
        user_id: User identifier
        
    Returns:
        User report with statistics and plots
    """
    # Fetch data
    user = fetch_user(user_id)
    all_posts = fetch_all_posts()
    posts = [p for p in all_posts if p.get("user_id") == user_id]
    
    report = {
        "user": user,
        "post_count": len(posts)
    }
    
    if not posts:
        return report
    
    # Extract engagement data
    titles = [p["title"] for p in posts]
    likes = [p.get("likes", 0) for p in posts]
    views = [p.get("views", 0) for p in posts]
    
    # Create likes bar chart
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    ax1.bar(range(len(titles)), likes, color='steelblue')
    ax1.set_xlabel('Post Index')
    ax1.set_ylabel('Likes')
    ax1.set_title(f'{user["name"]} - Likes')
    
    ax2.plot(range(len(titles)), views, marker='o', color='darkgreen', linewidth=2)
    ax2.set_xlabel('Post Index')
    ax2.set_ylabel('Views')
    ax2.set_title(f'{user["name"]} - Views')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    plot_path = f'reports/figures/user_{user_id}_report.png'
    os.makedirs('reports/figures', exist_ok=True)
    plt.savefig(plot_path)
    plt.close()
    
    report['engagement_plot'] = plot_path
    report['total_likes'] = sum(likes)
    report['total_views'] = sum(views)
    
    return report


def generate_category_report() -> Dict[str, Any]:
    """
    Generate report analyzing posts by category
    
    Returns:
        Category analysis report with plots
    """
    # Fetch data
    posts = fetch_all_posts()
    
    # Aggregate by category
    category_data = {}
    for post in posts:
        cat = post.get("category", "Uncategorized")
        if cat not in category_data:
            category_data[cat] = {"likes": [], "views": [], "count": 0}
        
        category_data[cat]["likes"].append(post.get("likes", 0))
        category_data[cat]["views"].append(post.get("views", 0))
        category_data[cat]["count"] += 1
    
    # Calculate averages
    categories = list(category_data.keys())
    avg_likes = [sum(category_data[c]["likes"]) / len(category_data[c]["likes"]) 
                 for c in categories]
    avg_views = [sum(category_data[c]["views"]) / len(category_data[c]["views"]) 
                 for c in categories]
    
    # Create grouped bar chart
    x = range(len(categories))
    width = 0.35
    
    plt.figure(figsize=(12, 6))
    plt.bar([i - width/2 for i in x], avg_likes, width, label='Avg Likes', color='steelblue')
    plt.bar([i + width/2 for i in x], avg_views, width, label='Avg Views', color='coral')
    
    plt.xlabel('Category')
    plt.ylabel('Average Count')
    plt.title('Category Performance')
    plt.xticks(x, categories, rotation=45, ha='right')
    plt.legend()
    plt.tight_layout()
    
    plot_path = 'reports/figures/category_performance.png'
    os.makedirs('reports/figures', exist_ok=True)
    plt.savefig(plot_path)
    plt.close()
    
    report = {
        "categories": {cat: {"count": data["count"],
                            "avg_likes": sum(data["likes"]) / len(data["likes"]),
                            "avg_views": sum(data["views"]) / len(data["views"])}
                      for cat, data in category_data.items()},
        "plot": plot_path
    }
    
    return report


def save_report_json(report_data: Dict[str, Any], filename: str) -> str:
    """
    Save report data to JSON file
    
    Args:
        report_data: Report data to save
        filename: Output filename
        
    Returns:
        Path to saved file
    """
    os.makedirs('reports', exist_ok=True)
    filepath = f'reports/{filename}'
    
    with open(filepath, 'w') as f:
        json.dump(report_data, f, indent=2)
    
    return filepath
