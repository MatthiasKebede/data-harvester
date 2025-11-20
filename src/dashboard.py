"""
Dashboard module for generating comprehensive reports and visualizations
"""

import tablib
import json
import os
import statistics
from typing import Dict, Any
from src.api_client import fetch_user, fetch_all_users, fetch_all_posts


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
    
    # Create data for overview metrics
    overview_dataset = tablib.Dataset()
    overview_dataset.headers = ['metric', 'value', 'type']
    overview_dataset.append(['Total Users', dashboard["total_users"], 'count'])
    overview_dataset.append(['Total Posts', dashboard["total_posts"], 'count'])
    overview_dataset.append(['Avg Posts/User', round(dashboard["avg_posts_per_user"], 2), 'average'])

    # Select only metric and value columns for export
    export_dataset = tablib.Dataset()
    export_dataset.headers = ['metric', 'value']
    for row in overview_dataset:
        export_dataset.append([row[0], row[1]])
    
    overview_csv = 'data/overview_metrics.csv'
    os.makedirs('data', exist_ok=True)
    with open(overview_csv, 'w', encoding='utf-8') as csvfile:
        csvfile.write(export_dataset.export('csv'))
    
    dashboard['overview_path'] = overview_csv
    
    return dashboard


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
            category_data[cat] = {"likes": [], "views": [], "post_count": 0}
        
        category_data[cat]["likes"].append(post.get("likes", 0))
        category_data[cat]["views"].append(post.get("views", 0))
        category_data[cat]["post_count"] += 1
    
    # Calculate averages
    performance_dataset = tablib.Dataset()
    performance_dataset.headers = ['category', 'post_count', 'avg_likes', 'avg_views', 'total_likes', 'total_views']
    
    category_stats = {}
    for cat, data in category_data.items():
        stats = {
            "post_count": data["post_count"],
            "avg_likes": statistics.mean(data["likes"]) if data["likes"] else 0,
            "avg_views": statistics.mean(data["views"]) if data["views"] else 0,
            "total_likes": sum(data["likes"]),
            "total_views": sum(data["views"])
        }
        category_stats[cat] = stats

        performance_dataset.append([
            cat,
            stats['post_count'],
            round(stats['avg_likes'], 2),
            round(stats['avg_views'], 2),
            stats['total_likes'],
            stats['total_views']
        ])
    
    # Export CSV file
    performance_csv = 'data/category_performance.csv'
    os.makedirs('data', exist_ok=True)
    with open(performance_csv, 'w', encoding='utf-8') as csvfile:
        csvfile.write(performance_dataset.export('csv'))
    
    report = {
        "categories": category_stats,
        "path": performance_csv
    }
    
    return report


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
