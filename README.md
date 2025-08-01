# DNS Lookup Tool

A simple, command-line DNS lookup tool that performs various DNS queries with clean, intuitive output.

## Features

- Multiple DNS record types (A, AAAA, MX, CNAME, NS, TXT, SOA)
- Single domain or bulk domain processing
- Clean formatted output (table/JSON options)
- Performance timing
- Custom DNS server support
- Error handling with meaningful messages

## Installation

```bash
git clone https://github.com/0x-Decrypt/dns-lookup
cd dns-lookup
pip install -r requirements.txt
```

## Usage

### Basic Examples

```bash
# Basic A record lookup
python dns_lookup.py google.com

# Specific record type
python dns_lookup.py google.com --type MX

# Multiple domains
python dns_lookup.py google.com facebook.com --type A

# Bulk processing from file
python dns_lookup.py --file domains.txt --output json

# Custom DNS server
python dns_lookup.py google.com --server 8.8.8.8
```

## Development

### Project Structure
```
dns-lookup/
├── src/
│   ├── dns_resolver.py     # Core DNS resolution logic
│   ├── output_formatter.py # Display formatting
│   ├── file_handler.py     # File I/O operations
│   └── cli.py             # Command-line interface
├── tests/
├── README.md
├── requirements.txt
└── dns_lookup.py          # Main entry point
```

### Running Tests
```bash
python -m pytest tests/
```

## License

MIT License - see LICENSE file for details.
