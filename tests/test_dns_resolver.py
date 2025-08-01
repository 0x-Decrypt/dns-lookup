"""
Test suite for DNS resolver functionality.
"""

import unittest
from unittest.mock import Mock, patch
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from dns_resolver import DNSResolver


class TestDNSResolver(unittest.TestCase):
    """Test cases for DNSResolver class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.resolver = DNSResolver()
    
    @patch('dns.resolver.Resolver.resolve')
    def test_successful_query(self, mock_resolve):
        """Test successful DNS query."""
        # Mock DNS response
        mock_record = Mock()
        mock_record.__str__ = Mock(return_value='192.168.1.1')
        mock_resolve.return_value = [mock_record]
        
        result = self.resolver.query_domain('example.com', 'A')
        
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['domain'], 'example.com')
        self.assertEqual(result['record_type'], 'A')
        self.assertEqual(result['records'], ['192.168.1.1'])
        self.assertGreater(result['query_time_ms'], 0)
    
    @patch('dns.resolver.Resolver.resolve')
    def test_domain_not_found(self, mock_resolve):
        """Test NXDOMAIN error handling."""
        import dns.resolver
        mock_resolve.side_effect = dns.resolver.NXDOMAIN()
        
        result = self.resolver.query_domain('nonexistent.com', 'A')
        
        self.assertEqual(result['status'], 'error')
        self.assertEqual(result['error'], 'Domain not found')
    
    @patch('dns.resolver.Resolver.resolve')
    def test_no_records_found(self, mock_resolve):
        """Test NoAnswer error handling."""
        import dns.resolver
        mock_resolve.side_effect = dns.resolver.NoAnswer()
        
        result = self.resolver.query_domain('example.com', 'MX')
        
        self.assertEqual(result['status'], 'error')
        self.assertEqual(result['error'], 'No MX records found')
    
    def test_mx_record_parsing(self):
        """Test MX record parsing."""
        with patch('dns.resolver.Resolver.resolve') as mock_resolve:
            mock_record = Mock()
            mock_record.preference = 10
            mock_record.exchange = 'mail.example.com'
            mock_resolve.return_value = [mock_record]
            
            result = self.resolver.query_domain('example.com', 'MX')
            
            self.assertEqual(result['records'], ['10 mail.example.com'])


if __name__ == '__main__':
    unittest.main()
