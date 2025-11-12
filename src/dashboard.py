"""
Dashboard module for generating comprehensive reports and visualizations
"""

import csv
import statistics
from typing import Dict, Any
import json
import os
from src.api_client import fetch_user, fetch_all_users, fetch_all_posts


BASE_URL = "http://localhost:3000"
TIMEOUT = 10


def generate_overview_dashboard() -> Dict[str, Any]:
    """
    Generate a dashboard with overview statistics and data exports
    
    Returns:
        Dashboard data with CSV file paths
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
    
    # Export overview metrics to CSV
    overview_csv = 'data/overview_metrics.csv'
    os.makedirs('data', exist_ok=True)
    with open(overview_csv, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['metric', 'value']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        writer.writerow({'metric': 'Total Users', 'value': dashboard["total_users"]})
        writer.writerow({'metric': 'Total Posts', 'value': dashboard["total_posts"]})
        writer.writerow({'metric': 'Avg Posts/User', 'value': round(dashboard["avg_posts_per_user"], 2)})
    
    dashboard['overview_path'] = overview_csv
    
    # Count posts per user
    user_post_counts = {}
    for post in posts:
        uid = post.get("user_id", "unknown")
        user_post_counts[uid] = user_post_counts.get(uid, 0) + 1
    
    # Export post distribution to CSV
    distribution_csv = 'data/posts_distribution.csv'
    with open(distribution_csv, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['user_id', 'post_count', 'percentage']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        total_posts = sum(user_post_counts.values())
        for uid, count in user_post_counts.items():
            percentage = (count / total_posts * 100) if total_posts > 0 else 0
            writer.writerow({
                'user_id': uid,
                'post_count': count,
                'percentage': round(percentage, 1)
            })
    
    dashboard['dist_path'] = distribution_csv

    return dashboard


def generate_user_report(user_id: str) -> Dict[str, Any]:
    """
    Generate detailed report for a specific user
    
    Args:
        user_id: User identifier
        
    Returns:
        User report with statistics and path to existing CSV file
    """
    from src.analyzer import analyze_user_activity

    # Get data from analysis
    analysis = analyze_user_activity(user_id)
    if "error" in analysis:
        return {"user": fetch_user(user_id), "post_count": 0}
    
    # Repackage the analysis results in report format
    report = {
        "user": fetch_user(user_id),
        "post_count": analysis["total_posts"],
        "path": analysis["path"],
        "total_likes": analysis["total_likes"],
        "total_views": analysis["total_views"],
        "avg_likes": analysis["avg_likes"],
        "avg_views": analysis["avg_views"]
    }
    
    return report


def generate_category_report() -> Dict[str, Any]:
    """
    Generate report analyzing posts by category
    
    Returns:
        Category analysis report with CSV data
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
    category_stats = {}
    for cat, data in category_data.items():
        category_stats[cat] = {
            "count": data["count"],
            "avg_likes": statistics.mean(data["likes"]) if data["likes"] else 0,
            "avg_views": statistics.mean(data["views"]) if data["views"] else 0,
            "total_likes": sum(data["likes"]),
            "total_views": sum(data["views"])
        }
    
    # Export category performance to CSV
    performance_csv = 'data/category_performance.csv'
    os.makedirs('data', exist_ok=True)
    with open(performance_csv, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['category', 'post_count', 'avg_likes', 'avg_views', 'total_likes', 'total_views']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for category, stats in category_stats.items():
            writer.writerow({
                'category': category,
                'post_count': stats['count'],
                'avg_likes': round(stats['avg_likes'], 2),
                'avg_views': round(stats['avg_views'], 2),
                'total_likes': stats['total_likes'],
                'total_views': stats['total_views']
            })
    
    report = {
        "categories": category_stats,
        "path": performance_csv
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
