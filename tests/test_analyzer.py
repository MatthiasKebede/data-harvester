"""
Tests for the analyzer module
"""

import matplotlib.pyplot as plt
from unittest.mock import patch
from src.analyzer import analyze_user_activity, analyze_post_distribution, analyze_engagement_trends


def test_analyze_user_activity(sample_user, sample_posts):
    """Test analyzing user activity with data fetching and plotting"""
    user_posts = [p for p in sample_posts if p["user_id"] == "1"]
    
    with patch('src.analyzer.fetch_user') as mock_fetch_user, \
         patch('src.analyzer.fetch_all_posts') as mock_fetch_posts, \
         patch('matplotlib.pyplot.savefig'), \
         patch('matplotlib.pyplot.close'):
        
        mock_fetch_user.return_value = sample_user
        mock_fetch_posts.return_value = sample_posts
        
        analysis = analyze_user_activity("1")
        
        assert analysis["user_name"] == "Alice Johnson"
        assert analysis["total_posts"] == 2
        assert "avg_likes" in analysis
        assert len(analysis["plots"]) == 2

        ax = plt.gca()
        lines = ax.get_lines()
        assert len(lines) > 0, "No line plot found"

        line_data = lines[0].get_ydata()
        expected_views = [p['views'] for p in user_posts]
        assert list(line_data) == expected_views
        assert 'Views' in ax.get_ylabel()
        assert 'Post Index' in ax.get_xlabel()
    plt.close('all')


def test_analyze_post_distribution(sample_posts):
    """Test analyzing post distribution by category"""
    with patch('src.analyzer.fetch_all_posts') as mock_fetch_posts, \
         patch('matplotlib.pyplot.savefig'), \
         patch('matplotlib.pyplot.close'):
        
        mock_fetch_posts.return_value = sample_posts
        
        analysis = analyze_post_distribution()
        
        assert "category_counts" in analysis
        assert "plot" in analysis
        assert "category_distribution.png" in analysis["plot"]

        ax = plt.gca()
        bars = ax.patches
        assert len(bars) > 0, "No bars found in plot"
        bar_heights = [int(bar.get_height()) for bar in bars]
        expected_counts = list(analysis["category_counts"].values())

        assert sorted(bar_heights) == sorted(expected_counts)
        assert 'Category' in ax.get_xlabel()
        assert 'Posts' in ax.get_ylabel()
    plt.close('all')

def test_analyze_engagement_trends(sample_posts):
    """Test that engagement scatter plot is created correctly"""
    with patch('src.analyzer.fetch_all_posts') as mock_fetch_posts, \
         patch('matplotlib.pyplot.savefig'), \
         patch('matplotlib.pyplot.close'):
        
        mock_fetch_posts.return_value = sample_posts
        
        plot_path = analyze_engagement_trends()
        assert plot_path == 'graphs/engagement_scatter.png'
        
        ax = plt.gca()
        collections = ax.collections
        assert len(collections) > 0, "No scatterplot found"
        scatter_data = collections[0].get_offsets()

        assert len(scatter_data) == len(sample_posts)
        assert 'Views' in ax.get_xlabel()
        assert 'Likes' in ax.get_ylabel()
    plt.close('all')
