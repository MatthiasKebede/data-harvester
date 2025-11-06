"""
Tests for visualizer module
"""

import pytest
import os
from src.visualizer import DataVisualizer


class TestDataVisualizer:
    """Test suite for DataVisualizer class"""

    @pytest.fixture
    def temp_output_dir(self, tmp_path):
        """Create a temporary output directory"""
        return str(tmp_path / "test_output")

    def test_initialization(self, temp_output_dir):
        """Test visualizer initialization"""
        visualizer = DataVisualizer(output_dir=temp_output_dir)
        assert visualizer.output_dir == temp_output_dir
        assert os.path.exists(temp_output_dir)
        assert visualizer.figure_count == 0

    def test_plot_bar_chart(self, temp_output_dir):
        """Test creating a bar chart"""
        visualizer = DataVisualizer(output_dir=temp_output_dir)
        data = {'Category A': 10, 'Category B': 20, 'Category C': 15}
        
        filepath = visualizer.plot_bar_chart(
            data,
            title="Test Bar Chart",
            xlabel="Categories",
            ylabel="Values",
            filename="test_bar.png"
        )
        
        assert os.path.exists(filepath)
        assert filepath.endswith("test_bar.png")

    def test_plot_line_chart(self, temp_output_dir):
        """Test creating a line chart"""
        visualizer = DataVisualizer(output_dir=temp_output_dir)
        data = {'Jan': 100, 'Feb': 150, 'Mar': 120, 'Apr': 180}
        
        filepath = visualizer.plot_line_chart(
            data,
            title="Test Line Chart",
            xlabel="Month",
            ylabel="Value",
            filename="test_line.png"
        )
        
        assert os.path.exists(filepath)
        assert visualizer.figure_count == 1

    def test_plot_pie_chart(self, temp_output_dir):
        """Test creating a pie chart"""
        visualizer = DataVisualizer(output_dir=temp_output_dir)
        data = {'Product A': 30, 'Product B': 45, 'Product C': 25}
        
        filepath = visualizer.plot_pie_chart(
            data,
            title="Test Pie Chart",
            filename="test_pie.png"
        )
        
        assert os.path.exists(filepath)

    def test_plot_histogram(self, temp_output_dir):
        """Test creating a histogram"""
        visualizer = DataVisualizer(output_dir=temp_output_dir)
        values = [1, 2, 2, 3, 3, 3, 4, 4, 5, 6, 7, 8, 9, 10]
        
        filepath = visualizer.plot_histogram(
            values,
            bins=5,
            title="Test Histogram",
            xlabel="Value",
            ylabel="Frequency",
            filename="test_hist.png"
        )
        
        assert os.path.exists(filepath)

    def test_plot_scatter(self, temp_output_dir):
        """Test creating a scatter plot"""
        visualizer = DataVisualizer(output_dir=temp_output_dir)
        x_values = [1, 2, 3, 4, 5]
        y_values = [2, 4, 5, 7, 9]
        
        filepath = visualizer.plot_scatter(
            x_values,
            y_values,
            title="Test Scatter",
            xlabel="X",
            ylabel="Y",
            filename="test_scatter.png"
        )
        
        assert os.path.exists(filepath)

    def test_plot_multiple_lines(self, temp_output_dir):
        """Test creating a multi-line chart"""
        visualizer = DataVisualizer(output_dir=temp_output_dir)
        datasets = {
            'Dataset 1': {'A': 10, 'B': 20, 'C': 15},
            'Dataset 2': {'A': 15, 'B': 25, 'C': 20}
        }
        
        filepath = visualizer.plot_multiple_lines(
            datasets,
            title="Test Multiple Lines",
            xlabel="Category",
            ylabel="Value",
            filename="test_multi_line.png"
        )
        
        assert os.path.exists(filepath)

    def test_auto_filename_generation(self, temp_output_dir):
        """Test automatic filename generation"""
        visualizer = DataVisualizer(output_dir=temp_output_dir)
        data = {'A': 10, 'B': 20}
        
        filepath1 = visualizer.plot_bar_chart(data)
        filepath2 = visualizer.plot_bar_chart(data)
        
        assert os.path.exists(filepath1)
        assert os.path.exists(filepath2)
        assert filepath1 != filepath2
        assert visualizer.figure_count == 2
