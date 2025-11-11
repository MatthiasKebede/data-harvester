"""
Tests for the dashboard module
"""

import matplotlib.pyplot as plt
from unittest.mock import patch
from src.dashboard import generate_overview_dashboard, generate_user_report


def test_generate_overview_dashboard(sample_users, sample_posts):
    """Test generating overview dashboard with fetching and plotting"""
    with patch('src.dashboard.fetch_all_users') as mock_fetch_all_users, \
         patch('src.dashboard.fetch_all_posts') as mock_fetch_posts, \
         patch('matplotlib.pyplot.savefig') as mock_savefig, \
         patch('matplotlib.pyplot.close'), \
         patch('os.makedirs'):
        
        mock_fetch_all_users.return_value = sample_users
        mock_fetch_posts.return_value = sample_posts
        
        dashboard = generate_overview_dashboard()
        
        assert dashboard["total_users"] == 3
        assert dashboard["total_posts"] == 5
        assert "overview_plot" in dashboard
        assert "pie_plot" in dashboard

        assert mock_savefig.call_count == 2
        save_calls = [call[0][0] for call in mock_savefig.call_args_list]
        assert 'reports/figures/overview.png' in save_calls
        assert 'reports/figures/posts_distribution.png' in save_calls
    plt.close('all')


def test_generate_user_report(sample_user, sample_posts):
    """Test generating user-specific report"""
    user_posts = [p for p in sample_posts if p["user_id"] == "1"]

    with patch('src.dashboard.fetch_user') as mock_fetch_user, \
         patch('src.dashboard.fetch_all_posts') as mock_fetch_posts, \
         patch('matplotlib.pyplot.savefig'), \
         patch('matplotlib.pyplot.close'), \
         patch('os.makedirs'):
        
        mock_fetch_user.return_value = sample_user
        mock_fetch_posts.return_value = sample_posts
        
        report = generate_user_report("1")
        
        assert report["user"]["name"] == "Alice Johnson"
        assert report["post_count"] == 2
        assert "engagement_plot" in report
        assert report["total_likes"] == sum([p["likes"] for p in user_posts])
        assert report["total_views"] == sum([p["views"] for p in user_posts])

        fig = plt.gcf()
        axes = fig.get_axes()
        assert len(axes) == 2, "Expected 2 subplots (likes and views)"
        
        # Check first subplot (likes bar chart)
        ax1 = axes[0]
        bars = ax1.patches
        assert len(bars) == 2, "Expected 2 bars for user's posts"
        bar_heights = [int(bar.get_height()) for bar in bars]
        expected_likes = [p["likes"] for p in user_posts]
        assert bar_heights == expected_likes
        assert 'Likes' in ax1.get_ylabel()
        assert 'Post Index' in ax1.get_xlabel()
        
        # Check second subplot (views line chart)
        ax2 = axes[1]
        lines = ax2.get_lines()
        assert len(lines) > 0, "No line plot found"
        line_data = lines[0].get_ydata()
        expected_views = [p["views"] for p in user_posts]
        assert list(line_data) == expected_views
        assert 'Views' in ax2.get_ylabel()
        assert 'Post Index' in ax2.get_xlabel()
    plt.close('all')
