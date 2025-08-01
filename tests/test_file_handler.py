"""
Test suite for file handler functionality.
"""

import unittest
import tempfile
import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from file_handler import FileHandler


class TestFileHandler(unittest.TestCase):
    """Test cases for FileHandler class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.temp_dir, 'test_domains.txt')
    
    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        os.rmdir(self.temp_dir)
    
    def test_read_domains_from_file(self):
        """Test reading domains from file."""
        domains_content = """# Test domains file
google.com
github.com
# This is a comment
stackoverflow.com

python.org"""
        
        with open(self.test_file, 'w') as f:
            f.write(domains_content)
        
        domains = FileHandler.read_domains_from_file(self.test_file)
        
        expected = ['google.com', 'github.com', 'stackoverflow.com', 'python.org']
        self.assertEqual(domains, expected)
    
    def test_read_nonexistent_file(self):
        """Test reading from nonexistent file."""
        with self.assertRaises(FileNotFoundError):
            FileHandler.read_domains_from_file('nonexistent.txt')
    
    def test_write_output_to_file(self):
        """Test writing output to file."""
        content = "Test output content"
        output_file = os.path.join(self.temp_dir, 'output.txt')
        
        result = FileHandler.write_output_to_file(content, output_file)
        
        self.assertTrue(result)
        self.assertTrue(os.path.exists(output_file))
        
        with open(output_file, 'r') as f:
            self.assertEqual(f.read(), content)
    
    def test_validate_file_path(self):
        """Test file path validation."""
        # Create test file
        with open(self.test_file, 'w') as f:
            f.write('test')
        
        self.assertTrue(FileHandler.validate_file_path(self.test_file))
        self.assertFalse(FileHandler.validate_file_path('nonexistent.txt'))


if __name__ == '__main__':
    unittest.main()
