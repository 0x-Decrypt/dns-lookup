"""
DNS resolver module for performing various DNS queries.
Handles all major DNS record types with clean error handling.
"""

import dns.resolver
import dns.exception
import time
from typing import List, Dict, Any, Optional, Union


class DNSResolver:
    """Handles DNS query operations with timing and error management."""
    
    def __init__(self, dns_server: Optional[str] = None):
        """Initialize resolver with optional custom DNS server."""
        self.resolver = dns.resolver.Resolver()
        if dns_server:
            self.resolver.nameservers = [dns_server]
    
    def query_domain(self, domain: str, record_type: str = 'A') -> Dict[str, Any]:
        """
        Query a single domain for specific record type.
        
        Args:
            domain: Domain name to query
            record_type: DNS record type (A, AAAA, MX, etc.)
            
        Returns:
            Dictionary containing query results and metadata
        """
        start_time = time.time()
        
        try:
            result = self.resolver.resolve(domain, record_type)
            records = self._parse_records(result, record_type)
            query_time = round((time.time() - start_time) * 1000, 2)
            
            return {
                'domain': domain,
                'record_type': record_type,
                'records': records,
                'query_time_ms': query_time,
                'status': 'success'
            }
            
        except dns.resolver.NXDOMAIN:
            return self._error_result(domain, record_type, 'Domain not found')
        except dns.resolver.NoAnswer:
            return self._error_result(domain, record_type, f'No {record_type} records found')
        except dns.resolver.Timeout:
            return self._error_result(domain, record_type, 'Query timeout')
        except Exception as e:
            return self._error_result(domain, record_type, f'Query failed: {str(e)}')
    
    def query_multiple_types(self, domain: str, record_types: List[str]) -> Dict[str, Any]:
        """Query domain for multiple record types simultaneously."""
        results = {}
        total_time = 0
        
        for record_type in record_types:
            result = self.query_domain(domain, record_type)
            results[record_type] = result
            if result['status'] == 'success':
                total_time += result['query_time_ms']
        
        return {
            'domain': domain,
            'results': results,
            'total_time_ms': round(total_time, 2)
        }
    
    def _parse_records(self, result: dns.resolver.Answer, record_type: str) -> List[str]:
        """Parse DNS response based on record type."""
        records = []
        
        for record in result:
            if record_type == 'MX':
                records.append(f"{record.preference} {record.exchange}")
            elif record_type == 'SOA':
                records.append(f"{record.mname} {record.rname} {record.serial}")
            else:
                records.append(str(record))
        
        return records
    
    def _error_result(self, domain: str, record_type: str, error_msg: str) -> Dict[str, Any]:
        """Create standardized error result."""
        return {
            'domain': domain,
            'record_type': record_type,
            'records': [],
            'query_time_ms': 0,
            'status': 'error',
            'error': error_msg
        }
