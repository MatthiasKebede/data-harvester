"""
Tests for the analyzer module
"""

import csv
import os
import pytest
from unittest.mock import patch
from src.analyzer import analyze_user_activity, analyze_engagement_trends


def test_analyze_user_activity(sample_user, sample_posts):
    """Test analyzing user activity with data fetching and plotting"""    
    with patch('src.analyzer.fetch_user') as mock_fetch_user, \
         patch('src.analyzer.fetch_all_posts') as mock_fetch_posts:
        
        mock_fetch_user.return_value = sample_user
        mock_fetch_posts.return_value = sample_posts

        analysis = analyze_user_activity("1")
        
        assert analysis["user"] == "Alice Johnson"
        assert analysis["total_posts"] == 2
        assert analysis["total_likes"] == 112
        assert analysis["total_views"] == 542

        assert os.path.exists("data/user_1_posts.csv")
        with open("data/user_1_posts.csv", 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)

            assert len(rows) == 2

            assert rows[0]['post_index'] == '1'
            assert rows[0]['title'] == 'Data Science Tips'
            assert float(rows[0]['likes']) == pytest.approx(67)
            assert float(rows[0]['views']) == pytest.approx(312)
            assert rows[0]['category'] == 'Technology'
            
            assert rows[1]['post_index'] == '0'
            assert rows[1]['title'] == 'Getting Started with Python'
            assert float(rows[1]['likes']) == pytest.approx(45)
            assert float(rows[1]['views']) == pytest.approx(230)
            assert rows[1]['category'] == 'Technology'


def test_analyze_engagement_trends(sample_posts):
    """Test that engagement scatter plot is created correctly"""
    with patch('src.analyzer.fetch_all_posts') as mock_fetch_posts:
        
        mock_fetch_posts.return_value = sample_posts

        csv_path = analyze_engagement_trends()
        
        assert csv_path == 'data/engagement_trends.csv'
        assert os.path.exists(csv_path)
        
        with open(csv_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)
            
            assert len(rows) == 5

            assert rows[0]['post_id'] == '1'
            assert rows[0]['title'] == 'Getting Started with Python'
            assert float(rows[0]['views']) == pytest.approx(230)
            assert float(rows[0]['likes']) == pytest.approx(45)
            assert float(rows[0]['engagement_ratio']) == pytest.approx(0.1957, abs=0.01)


def test_calculate_average_title_length(sample_posts):
    """Test calculating average post title length"""
    # TODO: Implement this test (Hint: the expected average is 18.8)
    pass
