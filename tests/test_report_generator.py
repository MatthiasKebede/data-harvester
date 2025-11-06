"""
Tests for report generator module
"""

import pytest
import os
import json
from src.report_generator import ReportGenerator


class TestReportGenerator:
    """Test suite for ReportGenerator class"""

    @pytest.fixture
    def temp_output_dir(self, tmp_path):
        """Create a temporary output directory"""
        return str(tmp_path / "test_reports")

    @pytest.fixture
    def sample_numeric_data(self):
        """Sample data with numeric fields"""
        return [
            {'id': '1', 'views': 100, 'likes': 10, 'category': 'tech'},
            {'id': '2', 'views': 150, 'likes': 20, 'category': 'tech'},
            {'id': '3', 'views': 200, 'likes': 30, 'category': 'science'},
            {'id': '4', 'views': 120, 'likes': 15, 'category': 'science'}
        ]

    def test_initialization(self, temp_output_dir):
        """Test report generator initialization"""
        generator = ReportGenerator(output_dir=temp_output_dir)
        assert generator.output_dir == temp_output_dir
        assert os.path.exists(temp_output_dir)
        assert generator.processor is not None
        assert generator.visualizer is not None

    def test_generate_summary_report(self, temp_output_dir, sample_numeric_data):
        """Test generating a summary report"""
        generator = ReportGenerator(output_dir=temp_output_dir)
        
        report = generator.generate_summary_report(
            sample_numeric_data,
            numeric_fields=['views', 'likes'],
            report_name='test_summary'
        )
        
        assert report['name'] == 'test_summary'
        assert report['total_records'] == 4
        assert 'views' in report['statistics']
        assert 'likes' in report['statistics']
        assert report['statistics']['views']['mean'] == 142.5
        assert len(report['visualizations']) > 0
        assert os.path.exists(report['report_path'])

    def test_summary_report_json_format(self, temp_output_dir, sample_numeric_data):
        """Test that summary report is saved as valid JSON"""
        generator = ReportGenerator(output_dir=temp_output_dir)
        
        report = generator.generate_summary_report(
            sample_numeric_data,
            numeric_fields=['views'],
            report_name='json_test'
        )
        
        # Read and verify JSON format
        with open(report['report_path'], 'r') as f:
            loaded_report = json.load(f)
        
        assert loaded_report['name'] == 'json_test'
        assert 'statistics' in loaded_report
