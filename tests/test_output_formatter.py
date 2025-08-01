"""
Test suite for output formatter functionality.
"""

import unittest
import json
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from output_formatter import OutputFormatter


class TestOutputFormatter(unittest.TestCase):
    """Test cases for OutputFormatter class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.success_result = {
            'domain': 'example.com',
            'record_type': 'A',
            'records': ['192.168.1.1', '192.168.1.2'],
            'query_time_ms': 45.2,
            'status': 'success'
        }
        
        self.error_result = {
            'domain': 'nonexistent.com',
            'record_type': 'A',
            'records': [],
            'query_time_ms': 0,
            'status': 'error',
            'error': 'Domain not found'
        }
    
    def test_format_table_success(self):
        """Test table formatting for successful result."""
        output = OutputFormatter.format_table(self.success_result)
        
        self.assertIn('example.com', output)
        self.assertIn('A Records:', output)
        self.assertIn('192.168.1.1', output)
        self.assertIn('192.168.1.2', output)
        self.assertIn('45.2ms', output)
    
    def test_format_table_error(self):
        """Test table formatting for error result."""
        output = OutputFormatter.format_table(self.error_result)
        
        self.assertIn('❌', output)
        self.assertIn('nonexistent.com', output)
        self.assertIn('Domain not found', output)
    
    def test_format_json(self):
        """Test JSON formatting."""
        results = [self.success_result, self.error_result]
        output = OutputFormatter._format_json(results)
        
        parsed = json.loads(output)
        self.assertIn('timestamp', parsed)
        self.assertEqual(parsed['total_queries'], 2)
        self.assertEqual(len(parsed['results']), 2)
    
    def test_format_summary(self):
        """Test summary statistics formatting."""
        results = [self.success_result, self.error_result]
        summary = OutputFormatter.format_summary(results)
        
        self.assertIn('1/2 successful', summary)
        self.assertIn('Failed: 1', summary)


if __name__ == '__main__':
    unittest.main()
