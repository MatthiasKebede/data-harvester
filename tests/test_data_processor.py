"""
Tests for data processor module
"""

import pytest
from src.data_processor import DataProcessor


class TestDataProcessor:
    """Test suite for DataProcessor class"""

    def test_clean_data(self):
        """Test that clean_data removes None values"""
        processor = DataProcessor()
        data = {'name': 'John', 'age': None, 'city': 'NYC'}
        cleaned = processor.clean_data(data)
        
        assert 'name' in cleaned
        assert 'city' in cleaned
        assert 'age' not in cleaned

    def test_aggregate_data(self, sample_posts_data):
        """Test data aggregation by key"""
        processor = DataProcessor()
        aggregated = processor.aggregate_data(sample_posts_data, 'user_id')
        
        assert '123' in aggregated
        assert '456' in aggregated
        assert len(aggregated['123']) == 2
        assert len(aggregated['456']) == 1

    def test_calculate_statistics(self, sample_posts_data):
        """Test statistical calculations"""
        processor = DataProcessor()
        stats = processor.calculate_statistics(sample_posts_data, 'views')
        
        assert stats['count'] == 3
        assert stats['mean'] == 150.0
        assert stats['median'] == 150.0
        assert stats['min'] == 100
        assert stats['max'] == 200
        assert stats['sum'] == 450

    def test_merge_data(self):
        """Test merging data with conflicting keys"""
        processor = DataProcessor()
        data1 = {'name': 'John', 'age': 30}
        data2 = {'name': 'Jane', 'city': 'NYC'}
        merged = processor.merge_data(data1, data2, prefix1='old', prefix2='new')
        
        assert 'old_name' in merged
        assert 'new_name' in merged
        assert merged['old_name'] == 'John'
        assert merged['new_name'] == 'Jane'
        assert merged['city'] == 'NYC'
