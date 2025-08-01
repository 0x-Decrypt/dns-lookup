"""
File handling module for DNS lookup tool.
Manages reading domain lists and writing output files.
"""

from typing import List, Optional
import os


class FileHandler:
    """Handles file I/O operations for the DNS lookup tool."""
    
    @staticmethod
    def read_domains_from_file(file_path: str) -> List[str]:
        """
        Read domain names from a text file.
        
        Args:
            file_path: Path to file containing domain names
            
        Returns:
            List of cleaned domain names
            
        Raises:
            FileNotFoundError: If file doesn't exist
            IOError: If file cannot be read
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        domains = []
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    domain = line.strip()
                    if domain and not domain.startswith('#'):
                        domains.append(domain)
        except IOError as e:
            raise IOError(f"Cannot read file {file_path}: {str(e)}")
        
        return domains
    
    @staticmethod
    def write_output_to_file(content: str, file_path: str) -> bool:
        """
        Write output content to file.
        
        Args:
            content: Content to write
            file_path: Output file path
            
        Returns:
            True if successful, False otherwise
        """
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            return True
        except IOError:
            return False
    
    @staticmethod
    def validate_file_path(file_path: str) -> bool:
        """Check if file path is valid and readable."""
        return os.path.exists(file_path) and os.path.isfile(file_path)
    
    @staticmethod
    def create_sample_domains_file(file_path: str) -> None:
        """Create a sample domains file for testing."""
        sample_domains = [
            "# Sample domains file for DNS lookup",
            "# Lines starting with # are ignored",
            "google.com",
            "github.com",
            "stackoverflow.com",
            "python.org"
        ]
        
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write('\n'.join(sample_domains))
