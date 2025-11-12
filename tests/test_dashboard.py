"""
Tests for the dashboard module
"""

import csv
import os
from unittest.mock import patch
from src.dashboard import generate_overview_dashboard, generate_user_report


def test_generate_overview_dashboard(sample_users, sample_posts):
    """Test generating overview dashboard with fetching and CSV export"""
    with patch('src.dashboard.fetch_all_users') as mock_fetch_all_users, \
         patch('src.dashboard.fetch_all_posts') as mock_fetch_posts:
        
        mock_fetch_all_users.return_value = sample_users
        mock_fetch_posts.return_value = sample_posts
        
        dashboard = generate_overview_dashboard()
        
        assert dashboard["total_users"] == 3
        assert dashboard["total_posts"] == 5
        assert "overview_path" in dashboard
        assert "dist_path" in dashboard

        assert os.path.exists(dashboard['overview_path'])
        with open(dashboard['overview_path'], 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)
            
            assert len(rows) == 3
            metrics = {row['metric']: row['value'] for row in rows}
            assert metrics['Total Users'] == '3'
            assert metrics['Total Posts'] == '5'
            assert float(metrics['Avg Posts/User']) == 1.67
        
        assert os.path.exists(dashboard['dist_path'])
        with open(dashboard['dist_path'], 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)
            
            assert len(rows) == 3

            user_data = {row['user_id']: int(row['post_count']) for row in rows}
            assert user_data['1'] == 2
            assert user_data['2'] == 2
            assert user_data['3'] == 1


def test_generate_user_report(sample_user, sample_posts):
    """Test generating user-specific report"""
    user_posts = [p for p in sample_posts if p["user_id"] == "1"]

    with patch('src.dashboard.fetch_user') as mock_fetch_user, \
         patch('src.analyzer.fetch_user') as mock_analyzer_user, \
         patch('src.analyzer.fetch_all_posts') as mock_analyzer_posts:
        
        mock_fetch_user.return_value = sample_user
        mock_analyzer_user.return_value = sample_user
        mock_analyzer_posts.return_value = sample_posts
        
        report = generate_user_report("1")
        
        assert "path" in report
        assert report["user"]["name"] == "Alice Johnson"
        assert report["post_count"] == 2
        assert report['path'] == 'data/user_1_posts.csv'
        assert report["total_likes"] == sum([p["likes"] for p in user_posts])
        assert report["total_views"] == sum([p["views"] for p in user_posts])
        
        assert os.path.exists(report['path'])
        with open(report['path'], 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)
            
            assert len(rows) == 2
            assert 'category' in rows[0]

            assert int(rows[0]['likes']) >= int(rows[1]['likes'])
            assert rows[0]['title'] == 'Data Science Tips'
            assert int(rows[0]['likes']) == 67
            assert int(rows[0]['views']) == 312
                        
            likes_from_csv = [int(row['likes']) for row in rows]
            views_from_csv = [int(row['views']) for row in rows]
            expected_likes = [p["likes"] for p in user_posts]
            expected_views = [p["views"] for p in user_posts]
            assert sorted(likes_from_csv) == sorted(expected_likes)
            assert sorted(views_from_csv) == sorted(expected_views)
