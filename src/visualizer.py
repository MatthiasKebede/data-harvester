"""
Data visualization module using matplotlib.
"""

import matplotlib.pyplot as plt
import matplotlib
from typing import Dict, Any, List, Optional, Tuple
import os

matplotlib.use('Agg')


class DataVisualizer:
    """
    Visualizer for creating charts and graphs from data
    """

    def __init__(self, output_dir: str = "output"):
        """
        Initialize the visualizer

        Args:
            output_dir: Directory to save generated plots
        """
        self.output_dir = output_dir
        self.figure_count = 0
        
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def plot_bar_chart(self, data: Dict[str, float], title: str = "Bar Chart",
                      xlabel: str = "Category", ylabel: str = "Value",
                      filename: Optional[str] = None) -> str:
        """
        Create a bar chart from data

        Args:
            data: Dictionary with categories as keys and values as numbers
            title: Chart title
            xlabel: X-axis label
            ylabel: Y-axis label
            filename: Optional filename to save the plot

        Returns:
            Path to saved plot file
        """
        plt.figure(figsize=(10, 6))
        categories = list(data.keys())
        values = list(data.values())
        
        plt.bar(categories, values, color='steelblue')
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        filepath = self._save_figure(filename)
        plt.close()
        
        return filepath

    def plot_line_chart(self, data: Dict[str, float], title: str = "Line Chart",
                       xlabel: str = "X", ylabel: str = "Y",
                       filename: Optional[str] = None) -> str:
        """
        Create a line chart from data

        Args:
            data: Dictionary with x-values as keys and y-values as numbers
            title: Chart title
            xlabel: X-axis label
            ylabel: Y-axis label
            filename: Optional filename to save the plot

        Returns:
            Path to saved plot file
        """
        plt.figure(figsize=(10, 6))
        x_values = list(data.keys())
        y_values = list(data.values())
        
        plt.plot(x_values, y_values, marker='o', linewidth=2, markersize=6, color='darkgreen')
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        filepath = self._save_figure(filename)
        plt.close()
        
        return filepath

    def plot_pie_chart(self, data: Dict[str, float], title: str = "Pie Chart",
                      filename: Optional[str] = None) -> str:
        """
        Create a pie chart from data

        Args:
            data: Dictionary with categories as keys and values as numbers
            title: Chart title
            filename: Optional filename to save the plot

        Returns:
            Path to saved plot file
        """
        plt.figure(figsize=(8, 8))
        labels = list(data.keys())
        sizes = list(data.values())
        
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        plt.title(title)
        plt.axis('equal')
        
        filepath = self._save_figure(filename)
        plt.close()
        
        return filepath

    def plot_histogram(self, values: List[float], bins: int = 10,
                      title: str = "Histogram", xlabel: str = "Value",
                      ylabel: str = "Frequency", filename: Optional[str] = None) -> str:
        """
        Create a histogram from a list of values

        Args:
            values: List of numeric values
            bins: Number of histogram bins
            title: Chart title
            xlabel: X-axis label
            ylabel: Y-axis label
            filename: Optional filename to save the plot

        Returns:
            Path to saved plot file
        """
        plt.figure(figsize=(10, 6))
        plt.hist(values, bins=bins, color='coral', edgecolor='black', alpha=0.7)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        plt.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        
        filepath = self._save_figure(filename)
        plt.close()
        
        return filepath

    def plot_scatter(self, x_values: List[float], y_values: List[float],
                    title: str = "Scatter Plot", xlabel: str = "X",
                    ylabel: str = "Y", filename: Optional[str] = None) -> str:
        """
        Create a scatter plot from two lists of values

        Args:
            x_values: List of x-axis values
            y_values: List of y-axis values
            title: Chart title
            xlabel: X-axis label
            ylabel: Y-axis label
            filename: Optional filename to save the plot

        Returns:
            Path to saved plot file
        """
        plt.figure(figsize=(10, 6))
        plt.scatter(x_values, y_values, alpha=0.6, s=50, color='purple')
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        filepath = self._save_figure(filename)
        plt.close()
        
        return filepath

    def plot_multiple_lines(self, datasets: Dict[str, Dict[str, float]],
                           title: str = "Multiple Lines",
                           xlabel: str = "X", ylabel: str = "Y",
                           filename: Optional[str] = None) -> str:
        """
        Create a line chart with multiple lines

        Args:
            datasets: Dictionary where keys are line labels and values are data dicts
            title: Chart title
            xlabel: X-axis label
            ylabel: Y-axis label
            filename: Optional filename to save the plot

        Returns:
            Path to saved plot file
        """
        plt.figure(figsize=(12, 6))
        
        for label, data in datasets.items():
            x_values = list(data.keys())
            y_values = list(data.values())
            plt.plot(x_values, y_values, marker='o', linewidth=2, label=label)
        
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        filepath = self._save_figure(filename)
        plt.close()
        
        return filepath

    def _save_figure(self, filename: Optional[str] = None) -> str:
        """
        Save the current figure to a file

        Args:
            filename: Optional filename, auto-generated if not provided

        Returns:
            Full path to saved file
        """
        self.figure_count += 1

        if filename is None:
            filename = f"figure_{self.figure_count}.png"
        
        filepath = os.path.join(self.output_dir, filename)
        plt.savefig(filepath, dpi=100, bbox_inches='tight')
        
        return filepath
