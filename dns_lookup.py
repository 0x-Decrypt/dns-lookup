#!/usr/bin/env python3
"""
DNS Lookup Tool - Main Entry Point

A simple command-line DNS lookup tool that performs various DNS queries
with clean, intuitive output.

Usage:
    python dns_lookup.py google.com
    python dns_lookup.py google.com --type MX
    python dns_lookup.py --file domains.txt
"""

import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.cli import DNSLookupCLI


def main():
    """Main entry point for the DNS lookup tool."""
    cli = DNSLookupCLI()
    exit_code = cli.run()
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
