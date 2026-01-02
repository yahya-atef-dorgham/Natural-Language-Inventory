"""Database connection and management."""
import sqlite3
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from config import config
from services.logging.logger import logger_instance as logger


class Database:
    """SQLite database connection manager."""
    
    def __init__(self, db_path: Optional[str] = None):
        """Initialize database connection."""
        self.db_path = db_path or config.DB_PATH
        self.conn: Optional[sqlite3.Connection] = None
        self._ensure_db_path()
    
    def _ensure_db_path(self):
        """Ensure database directory exists."""
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
    
    def connect(self) -> sqlite3.Connection:
        """Get or create database connection."""
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row  # Enable column access by name
            self._initialize_schema()
        return self.conn
    
    def _initialize_schema(self):
        """Initialize database schema and sample data."""
        try:
            cursor = self.conn.cursor()
            
            # Create inventory_items table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS inventory_items (
                    id TEXT PRIMARY KEY,
                    sku TEXT NOT NULL,
                    name TEXT NOT NULL,
                    category_id TEXT,
                    location_id TEXT,
                    current_stock INTEGER DEFAULT 0,
                    reorder_threshold INTEGER DEFAULT 0,
                    recent_sales_volume INTEGER DEFAULT 0,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create product_categories table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS product_categories (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    parent_category_id TEXT
                )
            ''')
            
            # Create locations table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS locations (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    type TEXT,
                    parent_location_id TEXT
                )
            ''')
            
            # Create indexes
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_inventory_items_category 
                ON inventory_items(category_id)
            ''')
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_inventory_items_location 
                ON inventory_items(location_id)
            ''')
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_inventory_items_stock 
                ON inventory_items(current_stock)
            ''')
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_inventory_items_sales 
                ON inventory_items(recent_sales_volume)
            ''')
            
            self.conn.commit()
            
            # Check if data exists
            cursor.execute('SELECT COUNT(*) as count FROM inventory_items')
            count = cursor.fetchone()['count']
            
            if count == 0:
                logger.info('Inserting sample data into database')
                self._insert_sample_data(cursor)
                self.conn.commit()
                logger.info('Sample data inserted successfully')
            
            logger.info('Database schema initialized', {'path': self.db_path})
            
        except Exception as e:
            logger.error('Failed to initialize database schema', {'error': str(e)})
            raise
    
    def _insert_sample_data(self, cursor: sqlite3.Cursor):
        """Insert sample data into database."""
        # Insert categories
        categories = [
            ('cat-1', 'Electronics', None),
            ('cat-2', 'Home & Garden', None),
            ('cat-3', 'Clothing', None),
        ]
        cursor.executemany(
            'INSERT OR IGNORE INTO product_categories (id, name, parent_category_id) VALUES (?, ?, ?)',
            categories
        )
        
        # Insert locations
        locations = [
            ('loc-1', 'Main Warehouse', 'warehouse'),
            ('loc-2', 'Store Downtown', 'store'),
            ('loc-3', 'Store Uptown', 'store'),
        ]
        cursor.executemany(
            'INSERT OR IGNORE INTO locations (id, name, type) VALUES (?, ?, ?)',
            locations
        )
        
        # Insert inventory items
        items = [
            ('item-1', 'ELEC-001', 'Laptop Computer', 'cat-1', 'loc-1', 50, 20, 150),
            ('item-2', 'ELEC-002', 'Smartphone', 'cat-1', 'loc-1', 30, 15, 200),
            ('item-3', 'ELEC-003', 'Tablet', 'cat-1', 'loc-2', 10, 10, 80),
            ('item-4', 'HOME-001', 'Garden Tool Set', 'cat-2', 'loc-1', 25, 10, 45),
            ('item-5', 'HOME-002', 'Lawn Mower', 'cat-2', 'loc-2', 5, 5, 30),
            ('item-6', 'CLOTH-001', 'T-Shirt', 'cat-3', 'loc-2', 100, 50, 300),
            ('item-7', 'CLOTH-002', 'Jeans', 'cat-3', 'loc-3', 75, 40, 250),
            ('item-8', 'ELEC-004', 'Headphones', 'cat-1', 'loc-1', 15, 10, 120),
            ('item-9', 'HOME-003', 'Plant Pot', 'cat-2', 'loc-1', 200, 100, 500),
            ('item-10', 'CLOTH-003', 'Jacket', 'cat-3', 'loc-3', 20, 15, 90),
        ]
        cursor.executemany(
            '''INSERT OR IGNORE INTO inventory_items 
               (id, sku, name, category_id, location_id, current_stock, reorder_threshold, recent_sales_volume) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
            items
        )
    
    def query(self, sql: str, params: Optional[List[Any]] = None) -> Dict[str, Any]:
        """Execute a query and return results."""
        if self.conn is None:
            self.connect()
        
        try:
            cursor = self.conn.cursor()
            
            # Convert SQL to SQLite format
            sqlite_sql = self._convert_to_sqlite(sql)
            
            if params:
                cursor.execute(sqlite_sql, params)
            else:
                cursor.execute(sqlite_sql)
            
            # Fetch all rows and convert to dictionaries
            rows = []
            for row in cursor.fetchall():
                rows.append(dict(row))
            
            return {'rows': rows}
            
        except Exception as e:
            logger.error('Query execution failed', {
                'error': str(e),
                'sql': sql[:200] if len(sql) > 200 else sql
            })
            raise
    
    def _convert_to_sqlite(self, sql: str) -> str:
        """Convert PostgreSQL-style SQL to SQLite-compatible SQL."""
        sqlite_sql = sql
        
        # Replace PostgreSQL double-quoted identifiers
        import re
        sqlite_sql = re.sub(r'as\s+"([^"]+)"', r'as \1', sqlite_sql, flags=re.IGNORECASE)
        
        # Replace NOW() with CURRENT_TIMESTAMP
        sqlite_sql = re.sub(r'NOW\(\)', "datetime('now')", sqlite_sql, flags=re.IGNORECASE)
        
        return sqlite_sql
    
    def test_connection(self) -> bool:
        """Test database connection."""
        try:
            if self.conn is None:
                self.connect()
            self.conn.execute('SELECT 1')
            logger.info('Database connection test successful')
            return True
        except Exception as e:
            logger.error('Database connection test failed', {'error': str(e)})
            return False
    
    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
            self.conn = None
            logger.info('Database connection closed')


# Global database instance
_db_instance: Optional[Database] = None


def get_database() -> Database:
    """Get or create database instance."""
    global _db_instance
    if _db_instance is None:
        _db_instance = Database()
        _db_instance.connect()
    return _db_instance


def query(sql: str, params: Optional[List[Any]] = None) -> Dict[str, Any]:
    """Execute a query using the global database instance."""
    db = get_database()
    return db.query(sql, params)


def test_connection() -> bool:
    """Test database connection."""
    db = get_database()
    return db.test_connection()

