"""
Tests for the dashboard module
"""

from unittest.mock import patch, Mock
from src.dashboard import generate_overview_dashboard, generate_user_report


def mock_response(json_data):
    """Helper to create mock response"""
    response = Mock()
    response.json.return_value = json_data
    response.raise_for_status.return_value = None
    return response


def test_generate_overview_dashboard(sample_users, sample_posts):
    """Test generating overview dashboard with fetching and plotting"""
    def get_side_effect(url, *args, **kwargs):
        if "/users" in url:
            return mock_response(sample_users)
        return mock_response(sample_posts)
    
    with patch('requests.get', side_effect=get_side_effect), \
         patch('matplotlib.pyplot.savefig'), \
         patch('matplotlib.pyplot.close'), \
         patch('os.makedirs'):
        
        dashboard = generate_overview_dashboard()
        
        assert dashboard["total_users"] == 3
        assert dashboard["total_posts"] == 5
        assert "overview_plot" in dashboard
        assert "pie_plot" in dashboard


def test_generate_user_report(sample_user, sample_posts):
    """Test generating user-specific report"""
    user_posts = [p for p in sample_posts if p["user_id"] == "1"]
    
    def get_side_effect(url, *args, **kwargs):
        if "/users/1" in url:
            return mock_response(sample_user)
        return mock_response(user_posts)
    
    with patch('requests.get', side_effect=get_side_effect), \
         patch('matplotlib.pyplot.savefig'), \
         patch('matplotlib.pyplot.close'), \
         patch('os.makedirs'):
        
        report = generate_user_report("1")
        
        assert report["user"]["name"] == "Alice Johnson"
        assert report["post_count"] == 2
        assert "engagement_plot" in report
