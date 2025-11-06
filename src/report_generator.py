"""
Report generation module for creating data reports with visualizations
"""

from typing import Dict, Any, List
from src.data_processor import DataProcessor
from src.visualizer import DataVisualizer
import json
import os


class ReportGenerator:
    """
    Generator for creating comprehensive data reports
    """

    def __init__(self, output_dir: str = "reports"):
        """
        Initialize the report generator

        Args:
            output_dir: Directory to save generated reports
        """
        self.output_dir = output_dir
        self.processor = DataProcessor()
        self.visualizer = DataVisualizer(output_dir=os.path.join(output_dir, "figures"))
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def generate_summary_report(self, data: List[Dict[str, Any]], 
                               numeric_fields: List[str],
                               report_name: str = "summary") -> Dict[str, Any]:
        """
        Generate a summary report with statistics for numeric fields

        Args:
            data: List of data dictionaries
            numeric_fields: List of numeric field names to analyze
            report_name: Name for the report

        Returns:
            Report dictionary with statistics and visualizations
        """
        report = {
            'name': report_name,
            'total_records': len(data),
            'statistics': {},
            'visualizations': []
        }
        
        for field in numeric_fields:
            stats = self.processor.calculate_statistics(data, field)
            report['statistics'][field] = stats
            
            # Create visualization for this field
            if stats['count'] > 0:
                chart_data = {
                    'Mean': stats['mean'],
                    'Median': stats['median'],
                    'Min': stats['min'],
                    'Max': stats['max']
                }
                chart_path = self.visualizer.plot_bar_chart(
                    chart_data,
                    title=f"{field.title()} Statistics",
                    xlabel="Metric",
                    ylabel="Value",
                    filename=f"{report_name}_{field}_stats.png"
                )
                report['visualizations'].append(chart_path)
        
        # Save report as JSON
        report_path = os.path.join(self.output_dir, f"{report_name}.json")
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        report['report_path'] = report_path
        return report
