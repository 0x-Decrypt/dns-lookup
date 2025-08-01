"""
Output formatting module for DNS lookup results.
Supports both table and JSON output formats.
"""

import json
from typing import Dict, Any, List
from datetime import datetime


class OutputFormatter:
    """Handles formatting of DNS query results for display."""
    
    @staticmethod
    def format_table(result: Dict[str, Any]) -> str:
        """Format single domain result as readable table."""
        if result['status'] == 'error':
            return f"❌ {result['domain']} ({result['record_type']}): {result['error']}\n"
        
        output = []
        output.append(f"DNS Lookup Results for: {result['domain']}")
        output.append("=" * (25 + len(result['domain'])))
        output.append(f"{result['record_type']} Records:")
        
        for record in result['records']:
            output.append(f"  {record}")
        
        output.append(f"\nQuery Time: {result['query_time_ms']}ms")
        output.append("")
        
        return "\n".join(output)
    
    @staticmethod
    def format_multiple_types(result: Dict[str, Any]) -> str:
        """Format multiple record types for single domain."""
        output = []
        output.append(f"DNS Lookup Results for: {result['domain']}")
        output.append("=" * (25 + len(result['domain'])))
        
        for record_type, type_result in result['results'].items():
            if type_result['status'] == 'success' and type_result['records']:
                output.append(f"\n{record_type} Records:")
                for record in type_result['records']:
                    output.append(f"  {record}")
            elif type_result['status'] == 'error':
                output.append(f"\n{record_type} Records: {type_result['error']}")
        
        output.append(f"\nTotal Query Time: {result['total_time_ms']}ms")
        output.append("")
        
        return "\n".join(output)
    
    @staticmethod
    def format_bulk_results(results: List[Dict[str, Any]], output_format: str = 'table') -> str:
        """Format multiple domain results."""
        if output_format == 'json':
            return OutputFormatter._format_json(results)
        
        output = []
        output.append(f"DNS Bulk Lookup Results ({len(results)} domains)")
        output.append("=" * 50)
        output.append("")
        
        for result in results:
            output.append(OutputFormatter.format_table(result))
        
        return "\n".join(output)
    
    @staticmethod
    def format_summary(results: List[Dict[str, Any]]) -> str:
        """Create summary statistics for bulk results."""
        total = len(results)
        successful = len([r for r in results if r['status'] == 'success'])
        failed = total - successful
        
        total_time = sum(r.get('query_time_ms', 0) for r in results)
        avg_time = round(total_time / total, 2) if total > 0 else 0
        
        summary = []
        summary.append(f"Summary: {successful}/{total} successful")
        summary.append(f"Failed: {failed}")
        summary.append(f"Average query time: {avg_time}ms")
        summary.append(f"Total time: {total_time}ms")
        
        return " | ".join(summary)
    
    @staticmethod
    def _format_json(results: List[Dict[str, Any]]) -> str:
        """Format results as JSON with metadata."""
        output = {
            'timestamp': datetime.now().isoformat(),
            'total_queries': len(results),
            'results': results
        }
        return json.dumps(output, indent=2)
