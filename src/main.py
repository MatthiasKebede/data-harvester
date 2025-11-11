"""
Main application orchestrator, coordinates the data harvesting workflow
"""

import os

from src.api_client import check_api_status, fetch_all_users
from src.analyzer import (
    analyze_user_activity,
    compare_users,
    analyze_post_distribution,
    analyze_engagement_trends
)
from src.dashboard import (
    generate_overview_dashboard,
    generate_user_report,
    generate_category_report,
    save_report_json
)


def main():
    """
    Main application entry point.
    Orchestrates data fetching, analysis, and dashboard generation.
    """
    print("Data Harvester Application")
    print("=" * 50)
    
    print("\nChecking API health...")
    if not check_api_status():
        print("ERROR: API is not responding. Please start json-server.")
        return
    print("API is healthy")
    
    # Create necessary directories
    os.makedirs("graphs", exist_ok=True)
    os.makedirs("reports", exist_ok=True)
    os.makedirs("reports/figures", exist_ok=True)
    
    print("\nFetching users...")
    users = fetch_all_users()
    print(f"Found {len(users)} users")
    for user in users:
        print(f"   - {user['name']} (ID: {user['id']})")
    
    # Analyze first user activity
    if users:
        user_id = users[0]["id"]
        print(f"\nAnalyzing activity for {users[0]['name']}...")
        activity = analyze_user_activity(user_id)
        if "error" not in activity:
            print(f"Total posts: {activity['total_posts']}")
            print(f"Average likes: {activity['avg_likes']:.1f}")
            print(f"Plots saved: {activity['plots']}")
    
    if len(users) >= 2:
        print("\nComparing users...")
        user_ids = [u["id"] for u in users[:2]]
        comparison_plot = compare_users(user_ids)
        print(f"Comparison plot saved: {comparison_plot}")
    
    print("\nAnalyzing post distribution...")
    distribution = analyze_post_distribution()
    print(f"Distribution plot saved: {distribution['plot']}")
    
    print("\nAnalyzing engagement trends...")
    trends_plot = analyze_engagement_trends()
    print(f"Trends plot saved: {trends_plot}")
    
    print("\nGenerating overview dashboard...")
    dashboard = generate_overview_dashboard()
    print(f"Total users: {dashboard['total_users']}")
    print(f"Total posts: {dashboard['total_posts']}")
    
    if users:
        print(f"\nGenerating user report for {users[0]['name']}...")
        user_report = generate_user_report(users[0]["id"])
        report_path = save_report_json(user_report, f"user_{users[0]['id']}_report.json")
        print(f"User report saved: {report_path}")
        if "engagement_plot" in user_report:
            print(f"Engagement plot: {user_report['engagement_plot']}")
    
    print("\nGenerating category report...")
    category_report = generate_category_report()
    report_path = save_report_json(category_report, "category_report.json")
    print(f"Category report saved: {report_path}")
    print(f"Category plot: {category_report['plot']}")
    
    print("\n" + "=" * 50)
    print("All operations completed successfully!")


if __name__ == "__main__":
    main()

