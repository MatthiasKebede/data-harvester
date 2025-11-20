"""
Tests for the dashboard module
"""

import csv
import os
import pytest
from unittest.mock import patch
from src.dashboard import generate_overview_dashboard, generate_category_report, generate_user_report


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

        assert os.path.exists(dashboard['overview_path'])
        with open(dashboard['overview_path'], 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)
            
            assert len(rows) == 3
            metrics = {row['metric']: row['value'] for row in rows}
            assert float(metrics['Total Users']) == pytest.approx(3)
            assert float(metrics['Total Posts']) == pytest.approx(5)
            assert float(metrics['Avg Posts/User']) == pytest.approx(1.67)


def test_generate_category_report(sample_posts):
    """Test generating category performance report with aggregation and CSV export"""
    with patch('src.dashboard.fetch_all_posts') as mock_fetch_posts:
        
        mock_fetch_posts.return_value = sample_posts
        
        report = generate_category_report()
        
        assert "categories" in report
        assert "path" in report
        assert report["path"] == 'data/category_performance.csv'
        
        categories = report["categories"]
        assert len(categories) == 3
        assert "Technology" in categories
        assert "Health" in categories
        
        tech = categories["Technology"]
        assert tech["post_count"] == 2
        assert tech["total_likes"] == 45 + 67
        assert tech["total_views"] == 230 + 312
        assert tech["avg_likes"] == 56
        assert tech["avg_views"] == 271
        
        assert os.path.exists(report['path'])
        with open(report['path'], 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)
            
            assert len(rows) == 3
            
            tech_row = next(r for r in rows if r['category'] == 'Technology')
            assert float(tech_row['post_count']) == pytest.approx(2)
            assert float(tech_row['avg_likes']) == pytest.approx(56)
            assert float(tech_row['avg_views']) == pytest.approx(271)
            assert float(tech_row['total_likes']) == pytest.approx(112)
            assert float(tech_row['total_views']) == pytest.approx(542)


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

            assert float(rows[0]['likes']) >= float(rows[1]['likes'])
            assert rows[0]['title'] == 'Data Science Tips'
            assert float(rows[0]['likes']) == pytest.approx(67)
            assert float(rows[0]['views']) == pytest.approx(312)
                        
            likes_from_csv = [float(row['likes']) for row in rows]
            views_from_csv = [float(row['views']) for row in rows]
            expected_likes = [float(p["likes"]) for p in user_posts]
            expected_views = [float(p["views"]) for p in user_posts]
            assert sorted(likes_from_csv) == sorted(expected_likes)
            assert sorted(views_from_csv) == sorted(expected_views)
