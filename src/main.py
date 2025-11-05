"""
Main entry point for the Data Harvester application
"""

from src.data_fetcher import DataFetcher
from src.data_processor import DataProcessor
from src.visualizer import DataVisualizer
from src.report_generator import ReportGenerator
from typing import Dict, Any, List


def fetch_and_process_user_data(base_url: str, user_id: str) -> Dict[str, Any]:
    """
    Fetch and process user data from API

    Args:
        base_url: Base URL of the API
        user_id: User identifier

    Returns:
        Processed user data
    """
    fetcher = DataFetcher(base_url=base_url)
    try:
        user_data = fetcher.fetch_user_data(user_id)
        return user_data
    finally:
        fetcher.close()


def fetch_and_analyze_posts(base_url: str, user_id: str = None, limit: int = 10) -> Dict[str, Any]:
    """
    Fetch posts and generate analysis report

    Args:
        base_url: Base URL of the API
        user_id: Optional user ID to filter posts
        limit: Maximum number of posts to fetch

    Returns:
        Analysis report with statistics
    """
    fetcher = DataFetcher(base_url=base_url)
    processor = DataProcessor()
    
    try:
        posts = fetcher.fetch_posts(user_id=user_id, limit=limit)
        
        # Calculate statistics if posts have numeric fields
        stats = {}
        if posts and 'views' in posts[0]:
            stats['views'] = processor.calculate_statistics(posts, 'views')
        if posts and 'likes' in posts[0]:
            stats['likes'] = processor.calculate_statistics(posts, 'likes')
        
        return {
            'total_posts': len(posts),
            'posts': posts,
            'statistics': stats
        }
    finally:
        fetcher.close()


def create_visualization_report(data: List[Dict[str, Any]], output_dir: str = "output") -> List[str]:
    """
    Create visualizations from data

    Args:
        data: List of data dictionaries
        output_dir: Directory to save visualizations

    Returns:
        List of paths to generated visualizations
    """
    visualizer = DataVisualizer(output_dir=output_dir)
    processor = DataProcessor()
    
    visualizations = []
    
    # Create bar chart if data has appropriate structure
    if data and isinstance(data, list):
        # Aggregate by a common field if available
        if 'category' in data[0]:
            aggregated = processor.aggregate_data(data, 'category')
            chart_data = {k: len(v) for k, v in aggregated.items()}
            
            path = visualizer.plot_bar_chart(
                chart_data,
                title="Data Distribution by Category",
                xlabel="Category",
                ylabel="Count"
            )
            visualizations.append(path)
    
    return visualizations


def generate_comprehensive_report(data: List[Dict[str, Any]], 
                                 numeric_fields: List[str],
                                 output_dir: str = "reports") -> Dict[str, Any]:
    """
    Generate a comprehensive report with statistics and visualizations

    Args:
        data: List of data dictionaries
        numeric_fields: List of numeric field names to analyze
        output_dir: Directory to save the report

    Returns:
        Complete report dictionary
    """
    generator = ReportGenerator(output_dir=output_dir)
    report = generator.generate_summary_report(data, numeric_fields)
    return report


if __name__ == "__main__":
    # Example usage
    print("Data Harvester Application")
    print("=" * 50)
    
    # Example: Fetch and process data
    example_base_url = "https://api.example.com"
    example_user_id = "12345"
    
    print(f"Fetching user data for user {example_user_id}...")
    # user_data = fetch_and_process_user_data(example_base_url, example_user_id)
    # print(f"User data fetched: {user_data}")
    
    print("\nData Harvester is ready to use")
