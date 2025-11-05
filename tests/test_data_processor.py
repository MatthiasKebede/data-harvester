"""
Tests for data processor module
"""

import pytest
from src.data_processor import DataProcessor


class TestDataProcessor:
    """Test suite for DataProcessor class"""

    def test_clean_data_removes_none_values(self):
        """Test that clean_data removes None values"""
        processor = DataProcessor()
        data = {'name': 'John', 'age': None, 'city': 'NYC'}
        cleaned = processor.clean_data(data)
        
        assert 'name' in cleaned
        assert 'city' in cleaned
        assert 'age' not in cleaned

    def test_clean_data_normalizes_keys(self):
        """Test that clean_data normalizes keys"""
        processor = DataProcessor()
        data = {'User-Name': 'John', 'User Age': 30}
        cleaned = processor.clean_data(data)
        
        assert 'user_name' in cleaned
        assert 'user_age' in cleaned
        assert cleaned['user_name'] == 'John'
        assert cleaned['user_age'] == 30

    def test_extract_fields(self):
        """Test extracting specific fields from data"""
        processor = DataProcessor()
        data = {'name': 'John', 'age': 30, 'city': 'NYC', 'country': 'USA'}
        extracted = processor.extract_fields(data, ['name', 'city'])
        
        assert len(extracted) == 2
        assert 'name' in extracted
        assert 'city' in extracted
        assert 'age' not in extracted

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

    def test_calculate_statistics_empty_data(self):
        """Test statistics with no valid data"""
        processor = DataProcessor()
        stats = processor.calculate_statistics([], 'views')
        
        assert stats['count'] == 0
        assert stats['mean'] == 0.0
        assert stats['sum'] == 0.0

    def test_filter_data(self, sample_posts_data):
        """Test filtering data by condition"""
        processor = DataProcessor()
        filtered = processor.filter_data(sample_posts_data, 'views', lambda x: x >= 150)
        
        assert len(filtered) == 2
        assert all(post['views'] >= 150 for post in filtered)

    def test_merge_data_no_conflicts(self):
        """Test merging data without conflicts"""
        processor = DataProcessor()
        data1 = {'name': 'John', 'age': 30}
        data2 = {'city': 'NYC', 'country': 'USA'}
        merged = processor.merge_data(data1, data2)
        
        assert len(merged) == 4
        assert merged['name'] == 'John'
        assert merged['city'] == 'NYC'

    def test_merge_data_with_conflicts(self):
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

    def test_processed_count(self):
        """Test processed item counter"""
        processor = DataProcessor()
        assert processor.get_processed_count() == 0
        
        processor.clean_data({'key': 'value'})
        processor.clean_data({'key': 'value'})
        
        assert processor.get_processed_count() == 2
        
        processor.reset_count()
        assert processor.get_processed_count() == 0
