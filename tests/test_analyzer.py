"""
Tests for the analyzer module
"""

import csv
import os
from unittest.mock import patch
from src.analyzer import analyze_user_activity, analyze_post_distribution, analyze_engagement_trends


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
            assert rows[0]['post_index'] == '0'
            assert rows[0]['title'] == 'Getting Started with Python'
            assert rows[0]['likes'] == '45'
            assert rows[0]['views'] == '230'
            assert rows[0]['category'] == 'Technology'


def test_analyze_post_distribution(sample_posts):
    """Test analyzing post distribution by category"""
    with patch('src.analyzer.fetch_all_posts') as mock_fetch_posts:
        
        mock_fetch_posts.return_value = sample_posts

        analysis = analyze_post_distribution()
        
        assert "category_counts" in analysis
        assert "path" in analysis
        assert analysis["path"] == "data/category_distribution.csv"
        
        assert analysis["category_counts"]["Technology"] == 2
        assert analysis["category_counts"]["Health"] == 2
        assert analysis["category_counts"]["Education"] == 1
        
        assert os.path.exists("data/category_distribution.csv")
        with open("data/category_distribution.csv", 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)
            
            assert len(rows) == 3
            category_data = {row['category']: int(row['post_count']) for row in rows}
            assert category_data['Technology'] == 2
            assert category_data['Health'] == 2
            assert category_data['Education'] == 1


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
            assert rows[0]['views'] == '230'
            assert rows[0]['likes'] == '45'
            assert float(rows[0]['engagement_ratio']) == 0.1957


def test_calculate_average_post_length(sample_posts):
    """Test calculating average post title length"""
    # TODO: Implement this test
    pass
