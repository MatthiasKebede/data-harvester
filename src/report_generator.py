"""
Report generation module for creating data reports with visualizations
"""

from typing import Dict, Any, List, Optional
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

    def generate_comparison_report(self, datasets: Dict[str, List[Dict[str, Any]]],
                                  field: str, report_name: str = "comparison") -> Dict[str, Any]:
        """
        Generate a comparison report between multiple datasets

        Args:
            datasets: Dictionary with dataset names as keys and data lists as values
            field: Field name to compare across datasets
            report_name: Name for the report

        Returns:
            Report dictionary with comparisons
        """
        report = {
            'name': report_name,
            'field': field,
            'datasets': {},
            'visualizations': []
        }
        
        # Calculate statistics for each dataset
        line_data = {}
        for dataset_name, data in datasets.items():
            stats = self.processor.calculate_statistics(data, field)
            report['datasets'][dataset_name] = stats
            line_data[dataset_name] = {
                'Mean': stats['mean'],
                'Median': stats['median']
            }
        
        # Create comparison visualization
        chart_path = self.visualizer.plot_multiple_lines(
            line_data,
            title=f"{field.title()} Comparison",
            xlabel="Metric",
            ylabel="Value",
            filename=f"{report_name}_{field}_comparison.png"
        )
        report['visualizations'].append(chart_path)
        
        # Save report as JSON
        report_path = os.path.join(self.output_dir, f"{report_name}.json")
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        report['report_path'] = report_path
        return report

    def generate_distribution_report(self, data: List[Dict[str, Any]],
                                    field: str, report_name: str = "distribution") -> Dict[str, Any]:
        """
        Generate a distribution report for a specific field

        Args:
            data: List of data dictionaries
            field: Field name to analyze distribution
            report_name: Name for the report

        Returns:
            Report dictionary with distribution analysis
        """
        report = {
            'name': report_name,
            'field': field,
            'statistics': {},
            'visualizations': []
        }
        
        # Extract values
        values = []
        for item in data:
            if field in item and isinstance(item[field], (int, float)):
                values.append(float(item[field]))
        
        if values:
            stats = self.processor.calculate_statistics(data, field)
            report['statistics'] = stats
            
            # Create histogram
            hist_path = self.visualizer.plot_histogram(
                values,
                bins=15,
                title=f"{field.title()} Distribution",
                xlabel=field.title(),
                ylabel="Frequency",
                filename=f"{report_name}_{field}_histogram.png"
            )
            report['visualizations'].append(hist_path)
        
        # Save report as JSON
        report_path = os.path.join(self.output_dir, f"{report_name}.json")
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        report['report_path'] = report_path
        return report
