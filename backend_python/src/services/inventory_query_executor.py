"""Inventory Query Executor - executes SQL queries safely."""
import re
import sys
import time
from pathlib import Path
from typing import List, Dict, Any

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.db.connection import query
from services.logging.logger import logger_instance as logger


class QueryResult:
    """Query result model."""
    def __init__(self, rows: List[Dict[str, Any]], row_count: int, execution_time_ms: int):
        self.rows = rows
        self.row_count = row_count
        self.execution_time_ms = execution_time_ms


class InventoryQueryExecutor:
    """Execute read-only SQL queries against the inventory database."""
    
    DANGEROUS_KEYWORDS = ['DROP', 'DELETE', 'UPDATE', 'INSERT', 'ALTER', 'CREATE', 'TRUNCATE']
    
    async def execute_query(self, sql: str) -> QueryResult:
        """Execute a read-only SQL query against the inventory database.
        
        This service ensures queries are safe and read-only.
        """
        start_time = time.time()
        logger.info('Executing inventory query', {'sql': sql})
        
        try:
            # Basic safety check: ensure query is SELECT only
            normalized_sql = sql.strip().upper()
            if not normalized_sql.startswith('SELECT'):
                raise ValueError('Only SELECT queries are allowed')
            
            # Check for dangerous keywords (as standalone words, not substrings)
            for keyword in self.DANGEROUS_KEYWORDS:
                keyword_regex = re.compile(rf'\b{keyword}\b', re.IGNORECASE)
                if keyword_regex.search(normalized_sql):
                    raise ValueError(f'Query contains forbidden keyword: {keyword}')
            
            # Convert PostgreSQL-style SQL to SQLite-compatible SQL
            sqlite_sql = self._convert_to_sqlite(sql)
            
            # Execute query
            result = query(sqlite_sql)
            execution_time_ms = int((time.time() - start_time) * 1000)
            
            # Map SQLite results to InventoryItem format
            rows = []
            for row in result['rows']:
                rows.append({
                    'id': row.get('id'),
                    'sku': row.get('sku'),
                    'name': row.get('name'),
                    'categoryId': row.get('categoryId') or row.get('category_id'),
                    'locationId': row.get('locationId') or row.get('location_id'),
                    'currentStock': row.get('currentStock') or row.get('current_stock') or 0,
                    'reorderThreshold': row.get('reorderThreshold') or row.get('reorder_threshold') or 0,
                    'recentSalesVolume': row.get('recentSalesVolume') or row.get('recent_sales_volume') or 0,
                    'createdAt': row.get('createdAt') or row.get('created_at'),
                    'updatedAt': row.get('updatedAt') or row.get('updated_at'),
                })
            
            logger.info('Query executed successfully', {
                'rowCount': len(rows),
                'executionTimeMs': execution_time_ms,
            })
            
            return QueryResult(
                rows=rows,
                row_count=len(rows),
                execution_time_ms=execution_time_ms
            )
        except Exception as e:
            execution_time_ms = int((time.time() - start_time) * 1000)
            logger.error('Query execution failed', {
                'error': str(e),
                'executionTimeMs': execution_time_ms,
            })
            raise
    
    def _convert_to_sqlite(self, sql: str) -> str:
        """Convert PostgreSQL-style SQL to SQLite-compatible SQL."""
        sqlite_sql = sql
        
        # Replace PostgreSQL double-quoted identifiers with SQLite square brackets or remove quotes
        sqlite_sql = re.sub(r'"([^"]+)"', r'\1', sqlite_sql)
        
        # Replace NOW() with CURRENT_TIMESTAMP if present
        sqlite_sql = re.sub(r'NOW\(\)', 'CURRENT_TIMESTAMP', sqlite_sql, flags=re.IGNORECASE)
        
        return sqlite_sql
    
    def map_to_chart_data(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Map database rows to chart-friendly format."""
        return [
            {
                'name': item.get('name', ''),
                'stock': item.get('currentStock', 0),
                'sales': item.get('recentSalesVolume', 0),
                'category': item.get('categoryId', ''),
            }
            for item in items
        ]


# Global instance
inventory_query_executor = InventoryQueryExecutor()

