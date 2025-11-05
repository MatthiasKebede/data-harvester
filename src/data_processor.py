"""
Data processing module for transforming and analyzing API data.
"""

from typing import Dict, Any, List
from datetime import datetime
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

    def extract_fields(self, data: Dict[str, Any], fields: List[str]) -> Dict[str, Any]:
        """
        Extract specific fields from data dictionary

        Args:
            data: Source data dictionary
            fields: List of field names to extract

        Returns:
            Dictionary containing only specified fields
        """
        extracted = {}
        for field in fields:
            if field in data:
                extracted[field] = data[field]
            else:
                # Try normalized version
                normalized_field = field.lower().replace(' ', '_').replace('-', '_')
                if normalized_field in data:
                    extracted[field] = data[normalized_field]
        
        return extracted

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

    def filter_data(self, data_list: List[Dict[str, Any]], 
                   field: str, condition: callable) -> List[Dict[str, Any]]:
        """
        Filter data based on a condition function

        Args:
            data_list: List of data dictionaries
            field: Field to apply condition to
            condition: Function that takes a value and returns bool

        Returns:
            Filtered list of data dictionaries
        """
        filtered = []
        for item in data_list:
            if field in item and condition(item[field]):
                filtered.append(item)
        
        return filtered

    def transform_dates(self, data: Dict[str, Any], date_fields: List[str], 
                       date_format: str = "%Y-%m-%d") -> Dict[str, Any]:
        """
        Transform date strings to datetime objects

        Args:
            data: Data dictionary
            date_fields: List of field names containing dates
            date_format: Date string format

        Returns:
            Data dictionary with transformed dates
        """
        transformed = data.copy()
        for field in date_fields:
            if field in transformed and isinstance(transformed[field], str):
                try:
                    transformed[field] = datetime.strptime(transformed[field], date_format)
                except ValueError:
                    # Keep original value if parsing fails
                    pass
        
        return transformed

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

    def get_processed_count(self) -> int:
        """
        Get the number of items processed

        Returns:
            Count of processed items
        """
        return self.processed_count

    def reset_count(self):
        """Reset the processed count to zero"""
        self.processed_count = 0
