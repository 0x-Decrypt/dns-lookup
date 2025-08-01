"""
Command-line interface for the DNS lookup tool.
Handles argument parsing and coordinates all operations.
"""

import argparse
import sys
from typing import List, Optional
from .dns_resolver import DNSResolver
from .output_formatter import OutputFormatter
from .file_handler import FileHandler


class DNSLookupCLI:
    """Command-line interface for DNS lookup operations."""
    
    SUPPORTED_RECORD_TYPES = ['A', 'AAAA', 'MX', 'CNAME', 'NS', 'TXT', 'SOA']
    
    def __init__(self):
        """Initialize CLI with argument parser."""
        self.parser = self._create_parser()
        self.resolver = None
    
    def run(self, args: Optional[List[str]] = None) -> int:
        """
        Main entry point for CLI execution.
        
        Args:
            args: Command line arguments (for testing)
            
        Returns:
            Exit code (0 for success, 1 for error)
        """
        try:
            parsed_args = self.parser.parse_args(args)
            self.resolver = DNSResolver(parsed_args.server)
            
            if parsed_args.file:
                return self._handle_file_input(parsed_args)
            elif parsed_args.domains:
                return self._handle_domain_input(parsed_args)
            else:
                self.parser.print_help()
                return 1
                
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            return 1
        except Exception as e:
            print(f"Error: {str(e)}")
            return 1
    
    def _create_parser(self) -> argparse.ArgumentParser:
        """Create and configure argument parser."""
        parser = argparse.ArgumentParser(
            description='DNS Lookup Tool - Query DNS records for domains',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=self._get_examples_text()
        )
        
        parser.add_argument(
            'domains',
            nargs='*',
            help='Domain names to query'
        )
        
        parser.add_argument(
            '-t', '--type',
            choices=self.SUPPORTED_RECORD_TYPES,
            default='A',
            help='DNS record type to query (default: A)'
        )
        
        parser.add_argument(
            '-f', '--file',
            help='File containing list of domains to query'
        )
        
        parser.add_argument(
            '-o', '--output',
            choices=['table', 'json'],
            default='table',
            help='Output format (default: table)'
        )
        
        parser.add_argument(
            '-s', '--server',
            help='Custom DNS server to use'
        )
        
        parser.add_argument(
            '--all-types',
            action='store_true',
            help='Query all supported record types'
        )
        
        parser.add_argument(
            '--output-file',
            help='Save output to file instead of stdout'
        )
        
        return parser
    
    def _handle_domain_input(self, args) -> int:
        """Handle direct domain input from command line."""
        results = []
        
        for domain in args.domains:
            if args.all_types:
                result = self.resolver.query_multiple_types(domain, self.SUPPORTED_RECORD_TYPES)
                output = OutputFormatter.format_multiple_types(result)
            else:
                result = self.resolver.query_domain(domain, args.type)
                results.append(result)
                output = OutputFormatter.format_table(result)
            
            if args.output_file:
                self._save_to_file(output, args.output_file)
            else:
                print(output, end='')
        
        if results and not args.all_types:
            summary = OutputFormatter.format_summary(results)
            print(f"\n{summary}")
        
        return 0
    
    def _handle_file_input(self, args) -> int:
        """Handle bulk domain processing from file."""
        try:
            domains = FileHandler.read_domains_from_file(args.file)
            print(f"Processing {len(domains)} domains from {args.file}...")
            
            results = []
            for i, domain in enumerate(domains, 1):
                print(f"Progress: {i}/{len(domains)}", end='\r')
                result = self.resolver.query_domain(domain, args.type)
                results.append(result)
            
            print()  # New line after progress
            
            output = OutputFormatter.format_bulk_results(results, args.output)
            summary = OutputFormatter.format_summary(results)
            
            full_output = f"{output}\n{summary}"
            
            if args.output_file:
                self._save_to_file(full_output, args.output_file)
                print(f"Results saved to {args.output_file}")
            else:
                print(full_output)
            
            return 0
            
        except FileNotFoundError as e:
            print(f"Error: {str(e)}")
            return 1
    
    def _save_to_file(self, content: str, file_path: str) -> None:
        """Save content to file with error handling."""
        if not FileHandler.write_output_to_file(content, file_path):
            print(f"Warning: Could not save output to {file_path}")
    
    def _get_examples_text(self) -> str:
        """Get examples section for help text."""
        return """
Examples:
  dns_lookup.py google.com                    # Basic A record lookup
  dns_lookup.py google.com --type MX          # MX record lookup
  dns_lookup.py google.com facebook.com       # Multiple domains
  dns_lookup.py --file domains.txt            # Bulk processing
  dns_lookup.py google.com --all-types        # All record types
  dns_lookup.py google.com --server 8.8.8.8   # Custom DNS server
  dns_lookup.py google.com --output json      # JSON output format
        """
