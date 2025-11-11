"""
Tests for the main module
"""

from unittest.mock import patch, MagicMock
from src.main import main


def create_mock_context(sample_users, analyze_return=None, overview_return=None):
    """Helper to create a common mock context for main tests"""
    analyze_return = analyze_return or {
        "total_posts": 2,
        "avg_likes": 45.5,
        "plots": ["graph1.png", "graph2.png"]
    }
    overview_return = overview_return or {
        "total_users": len(sample_users),
        "total_posts": 5,
        "overview_plot": "overview.png",
        "pie_plot": "pie.png"
    }
    
    # Create a mock manager to group all patches
    patcher = MagicMock()
    patcher.check_api_status.return_value = True
    patcher.fetch_users.return_value = sample_users
    patcher.analyze_user_activity.return_value = analyze_return
    patcher.compare_users.return_value = "comparison.png"
    patcher.analyze_post_distribution.return_value = {"plot": "distribution.png"}
    patcher.analyze_engagement_trends.return_value = "trends.png"
    patcher.generate_overview_dashboard.return_value = overview_return
    patcher.generate_user_report.return_value = {
        "user": sample_users[0],
        "engagement_plot": "user_report.png"
    }
    patcher.generate_category_report.return_value = {"plot": "category.png"}
    patcher.save_report_json.return_value = "reports/test.json"
    
    return patcher


def test_main_success(sample_users, capsys):
    """Test main function with successful execution"""
    mocks = create_mock_context(sample_users)
    
    with patch('src.api_client.check_api_status', mocks.check_api_status), \
         patch('src.api_client.fetch_users', mocks.fetch_users), \
         patch('src.analyzer.analyze_user_activity', mocks.analyze_user_activity), \
         patch('src.analyzer.compare_users', mocks.compare_users), \
         patch('src.analyzer.analyze_post_distribution', mocks.analyze_post_distribution), \
         patch('src.analyzer.analyze_engagement_trends', mocks.analyze_engagement_trends), \
         patch('src.dashboard.generate_overview_dashboard', mocks.generate_overview_dashboard), \
         patch('src.dashboard.generate_user_report', mocks.generate_user_report), \
         patch('src.dashboard.generate_category_report', mocks.generate_category_report), \
         patch('src.dashboard.save_report_json', mocks.save_report_json), \
         patch('os.makedirs'):
        
        main()
        captured = capsys.readouterr()
        assert "All operations completed successfully" in captured.out


def test_main_api_failure(capsys):
    """Test main function when API is down"""
    with patch('src.main.check_api_status', return_value=False):
        main()
        captured = capsys.readouterr()
        assert "ERROR" in captured.out
        assert "not responding" in captured.out
