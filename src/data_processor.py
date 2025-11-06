"""
Data processing module for transforming and analyzing API data.
"""

from typing import Dict, Any, List
import statistics


class DataProcessor:
    """
    Processor for cleaning, transforming, and analyzing data from APIs
    """

    def __init__(self):
        """Initialize the data processor"""
        self.processed_count = 0

    def clean_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Clean and normalize data by removing null values and standardizing keys

        Args:
            data: Raw data dictionary

        Returns:
            Cleaned data dictionary
        """
        cleaned = {}
        for key, value in data.items():
            if value is not None:
                # Normalize keys to lowercase with underscores
                normalized_key = key.lower().replace(' ', '_').replace('-', '_')
                cleaned[normalized_key] = value
        
        self.processed_count += 1
        return cleaned

    def aggregate_data(self, data_list: List[Dict[str, Any]], key: str) -> Dict[str, List[Any]]:
        """
        Aggregate data by grouping values under a common key

        Args:
            data_list: List of data dictionaries
            key: Key to aggregate by

        Returns:
            Dictionary with aggregated values
        """
        aggregated = {}
        for item in data_list:
            if key in item:
                group_key = str(item[key])
                if group_key not in aggregated:
                    aggregated[group_key] = []
                aggregated[group_key].append(item)
        
        return aggregated

    def calculate_statistics(self, data: List[Dict[str, Any]], numeric_field: str) -> Dict[str, float]:
        """
        Calculate statistics for a numeric field across multiple data items

        Args:
            data: List of data dictionaries
            numeric_field: Name of the numeric field to analyze

        Returns:
            Dictionary with statistical measures
        """
        values = []
        for item in data:
            if numeric_field in item and isinstance(item[numeric_field], (int, float)):
                values.append(float(item[numeric_field]))
        
        if not values:
            return {
                'count': 0,
                'mean': 0.0,
                'median': 0.0,
                'min': 0.0,
                'max': 0.0,
                'sum': 0.0
            }
        
        return {
            'count': len(values),
            'mean': statistics.mean(values),
            'median': statistics.median(values),
            'min': min(values),
            'max': max(values),
            'sum': sum(values)
        }

    def merge_data(self, data1: Dict[str, Any], data2: Dict[str, Any], 
                  prefix1: str = "source1", prefix2: str = "source2") -> Dict[str, Any]:
        """
        Merge two data dictionaries with prefixed keys for conflicts

        Args:
            data1: First data dictionary
            data2: Second data dictionary
            prefix1: Prefix for conflicting keys from data1
            prefix2: Prefix for conflicting keys from data2

        Returns:
            Merged dictionary
        """
        merged = {}
        
        # Add all items from data1
        for key, value in data1.items():
            if key in data2 and data2[key] != value:
                merged[f"{prefix1}_{key}"] = value
            else:
                merged[key] = value
        
        # Add remaining items from data2
        for key, value in data2.items():
            if key in data1 and data1[key] != value:
                merged[f"{prefix2}_{key}"] = value
            elif key not in merged:
                merged[key] = value
        
        return merged
