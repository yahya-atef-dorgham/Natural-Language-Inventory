"""Natural Language Query Draft Service with Reflection Pattern."""
import json
import re
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional
from openai import OpenAI

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import config
from services.logging.logger import logger_instance as logger


class DraftQuery:
    """Draft query model."""
    def __init__(self, sql: str, intent: str, entities: List[str], 
                 filters: Dict[str, Any], reasoning: Optional[str] = None,
                 critique: Optional[str] = None, revised: bool = False):
        self.sql = sql
        self.intent = intent
        self.entities = entities
        self.filters = filters
        self.reasoning = reasoning
        self.critique = critique
        self.revised = revised


class NLQueryDraftService:
    """Service for generating SQL queries from natural language using GPT."""
    
    DATABASE_SCHEMA = """
Database Schema for SQLite:

Table: inventory_items
Columns:
- id TEXT PRIMARY KEY
- sku TEXT NOT NULL (Stock Keeping Unit)
- name TEXT NOT NULL (Product name)
- category_id TEXT (Foreign key to product_categories.id)
- location_id TEXT (Foreign key to locations.id)
- current_stock INTEGER (Current quantity in stock)
- reorder_threshold INTEGER (Minimum stock level before reordering)
- recent_sales_volume INTEGER (Sales volume for recent period)
- created_at TEXT (Timestamp)
- updated_at TEXT (Timestamp)

Table: product_categories
Columns:
- id TEXT PRIMARY KEY
- name TEXT NOT NULL (Category name: 'Electronics', 'Clothing', 'Home & Garden')
- parent_category_id TEXT (For hierarchical categories)

Table: locations
Columns:
- id TEXT PRIMARY KEY
- name TEXT NOT NULL (Location name: 'Main Warehouse', 'Store Downtown', 'Store Uptown')
- type TEXT (Location type: 'warehouse', 'store')
- parent_location_id TEXT (For hierarchical locations)

Sample Data:
- Electronics products: 'Laptop Computer', 'Smartphone', 'Tablet', 'Headphones' (category_id='cat-1')
- Clothing products: 'T-Shirt', 'Jeans', 'Jacket' (category_id='cat-3')
- Home & Garden products: 'Garden Tool Set', 'Lawn Mower', 'Plant Pot' (category_id='cat-2')

CRITICAL SQL Rules for SQLite:
1. ONLY SELECT queries allowed - NO modifications
2. Use simple table aliases: i for inventory_items, c for product_categories, l for locations
3. Always use LEFT JOIN for optional relationships
4. Column aliases MUST use camelCase: current_stock as currentStock
5. WHERE clauses must use exact column names from schema
6. Category filter example: WHERE c.name = 'Electronics'
7. Always include these columns in SELECT: i.id, i.sku, i.name, i.category_id as categoryId, i.location_id as locationId, i.current_stock as currentStock, i.reorder_threshold as reorderThreshold, i.recent_sales_volume as recentSalesVolume
8. Default LIMIT 50, Maximum LIMIT 100
9. SQLite syntax only - no PostgreSQL-specific functions

Example Query:
SELECT i.id, i.sku, i.name, i.category_id as categoryId, i.current_stock as currentStock
FROM inventory_items i
LEFT JOIN product_categories c ON i.category_id = c.id
WHERE c.name = 'Electronics'
ORDER BY i.recent_sales_volume DESC
LIMIT 10;
"""
    
    def __init__(self):
        """Initialize the service with OpenAI client if configured."""
        self.openai: Optional[OpenAI] = None
        
        if config.openai.API_KEY and config.openai.ENABLED:
            if config.openai.IS_AZURE:
                # Azure OpenAI configuration
                # The endpoint might be a full URL or just the base
                # Extract base URL (remove /chat/completions and query params if present)
                endpoint = config.openai.ENDPOINT.rstrip('/')
                # Remove /chat/completions if present
                if '/chat/completions' in endpoint:
                    endpoint = endpoint.split('/chat/completions')[0]
                # Remove query parameters
                if '?' in endpoint:
                    endpoint = endpoint.split('?')[0]
                
                # Construct base_url: endpoint should be like https://xxx.openai.azure.com
                # We need: https://xxx.openai.azure.com/openai/deployments/{deployment}
                if '/openai/deployments' not in endpoint:
                    base_url = f"{endpoint}/openai/deployments/{config.openai.DEPLOYMENT}"
                else:
                    base_url = endpoint
                
                try:
                    # Initialize Azure OpenAI client
                    # For Azure OpenAI, we need to use the deployment name as the model
                    # and set up the base_url correctly
                    import os
                    # Temporarily disable proxies to avoid httpx compatibility issues
                    os.environ.pop('HTTP_PROXY', None)
                    os.environ.pop('HTTPS_PROXY', None)
                    os.environ.pop('http_proxy', None)
                    os.environ.pop('https_proxy', None)
                    
                    self.openai = OpenAI(
                        api_key=config.openai.API_KEY,
                        base_url=base_url,
                        default_query={'api-version': config.openai.API_VERSION},
                    )
                    logger.info('Azure OpenAI GPT integration enabled', {
                        'deployment': config.openai.DEPLOYMENT,
                        'endpoint': config.openai.ENDPOINT,
                        'base_url': base_url,
                    })
                except Exception as e:
                    logger.error(f'Failed to initialize Azure OpenAI client: {e}', {'error_type': type(e).__name__})
                    logger.warn('Falling back to keyword-based query generation')
                    self.openai = None
            else:
                # Standard OpenAI configuration
                try:
                    self.openai = OpenAI(api_key=config.openai.API_KEY)
                    logger.info('OpenAI GPT integration enabled', {'model': config.openai.MODEL})
                except Exception as e:
                    logger.error(f'Failed to initialize OpenAI client: {e}', {'error_type': type(e).__name__})
                    logger.warn('Falling back to keyword-based query generation')
                    self.openai = None
        else:
            logger.warn('OpenAI GPT disabled - using keyword-based fallback')
    
    async def generate_draft(self, natural_language_query: str) -> DraftQuery:
        """Generate a draft SQL query from natural language input using GPT.
        
        Implements Reflection Pattern: Draft → Self-Review → Finalize
        """
        logger.info('Generating draft query', {
            'query': natural_language_query,
            'usingGPT': self.openai is not None
        })
        
        # Try GPT-based generation if available
        if self.openai:
            try:
                # Step 1: Generate initial draft with GPT
                draft = await self._generate_with_gpt(natural_language_query)
                
                # Step 2: Self-review and critique the draft
                critique = await self._critique_query(natural_language_query, draft)
                
                # Step 3: Revise if necessary based on critique
                if critique['needsRevision']:
                    logger.info('Query needs revision', {'reason': critique['issues']})
                    revised = await self._revise_query(natural_language_query, draft, critique)
                    return DraftQuery(
                        sql=revised.sql,
                        intent=revised.intent,
                        entities=revised.entities,
                        filters=revised.filters,
                        reasoning=revised.reasoning,
                        critique='; '.join(critique['issues']),
                        revised=True
                    )
                
                return DraftQuery(
                    sql=draft.sql,
                    intent=draft.intent,
                    entities=draft.entities,
                    filters=draft.filters,
                    reasoning=draft.reasoning,
                    critique='No issues found',
                    revised=False
                )
            except Exception as e:
                logger.error('GPT generation failed, falling back to keyword-based', {
                    'error': str(e)
                })
                return self._generate_with_keywords(natural_language_query)
        
        # Fallback to keyword-based generation
        return self._generate_with_keywords(natural_language_query)
    
    async def _generate_with_gpt(self, natural_language_query: str) -> DraftQuery:
        """Generate SQL using GPT (Step 1: Draft)."""
        model_or_deployment = config.openai.DEPLOYMENT if config.openai.IS_AZURE else config.openai.MODEL
        
        completion = self.openai.chat.completions.create(
            model=model_or_deployment,
            messages=[
                {
                    'role': 'system',
                    'content': f"""You are an expert SQL query generator for an inventory management system.

{self.DATABASE_SCHEMA}

Your task:
1. Convert natural language queries to SELECT-only SQL queries
2. Use proper JOINs to include category and location names
3. Apply appropriate filters, sorting, and limits
4. Return results in JSON format with:
   - sql: The SQL query
   - intent: The query intent (e.g., 'top_sellers', 'low_stock', 'list_items')
   - filters: Object with detected filters (e.g., {{category: 'Electronics'}})
   - reasoning: Brief explanation of your approach

Security Rules:
- ONLY SELECT queries are allowed
- NO INSERT, UPDATE, DELETE, DROP, ALTER, CREATE, or other modification statements
- Use parameterized queries when possible
- Validate all inputs"""
                },
                {
                    'role': 'user',
                    'content': natural_language_query,
                },
            ],
            response_format={'type': 'json_object'},
            temperature=0.3
        )
        
        response = json.loads(completion.choices[0].message.content or '{}')
        
        logger.info('GPT generated SQL', {
            'sql': response.get('sql', ''),
            'intent': response.get('intent', ''),
            'reasoning': response.get('reasoning', ''),
        })
        
        return DraftQuery(
            sql=response.get('sql', ''),
            intent=response.get('intent', 'unknown'),
            entities=['InventoryItem'],
            filters=response.get('filters', {}),
            reasoning=response.get('reasoning', '')
        )
    
    async def _critique_query(self, natural_language_query: str, draft: DraftQuery) -> Dict[str, Any]:
        """Critique and review the generated query (Step 2: Self-Review)."""
        model_or_deployment = config.openai.DEPLOYMENT if config.openai.IS_AZURE else config.openai.MODEL
        
        completion = self.openai.chat.completions.create(
            model=model_or_deployment,
            messages=[
                {
                    'role': 'system',
                    'content': f"""You are a SQL query reviewer. Review the SQL query for:

1. **Security**: Ensure it's SELECT-only, no dangerous operations
2. **Correctness**: Check syntax, table/column names, JOINs
3. **Performance**: Verify appropriate indexes are used, LIMIT clauses exist
4. **Intent Alignment**: Ensure query matches the user's request

{self.DATABASE_SCHEMA}

Return JSON with:
- needsRevision: boolean
- issues: array of strings (empty if no issues)
- suggestions: array of improvements (if any)"""
                },
                {
                    'role': 'user',
                    'content': f"""User Query: "{natural_language_query}"

Generated SQL:
{draft.sql}

Review this query and identify any issues."""
                },
            ],
            response_format={'type': 'json_object'},
            temperature=0.2
        )
        
        review = json.loads(completion.choices[0].message.content or '{}')
        
        return {
            'needsRevision': review.get('needsRevision', False),
            'issues': review.get('issues', [])
        }
    
    async def _revise_query(self, natural_language_query: str, draft: DraftQuery,
                           critique: Dict[str, Any]) -> DraftQuery:
        """Revise the query based on critique (Step 3: Finalize)."""
        model_or_deployment = config.openai.DEPLOYMENT if config.openai.IS_AZURE else config.openai.MODEL
        
        completion = self.openai.chat.completions.create(
            model=model_or_deployment,
            messages=[
                {
                    'role': 'system',
                    'content': f"""You are an expert SQL query generator. Revise the SQL query to address the identified issues.

{self.DATABASE_SCHEMA}

Return JSON with the corrected query in the same format as before."""
                },
                {
                    'role': 'user',
                    'content': f"""User Query: "{natural_language_query}"

Original SQL:
{draft.sql}

Issues Found:
{chr(10).join(critique['issues'])}

Generate a corrected SQL query that addresses these issues."""
                },
            ],
            response_format={'type': 'json_object'},
            temperature=0.3
        )
        
        response = json.loads(completion.choices[0].message.content or '{}')
        
        return DraftQuery(
            sql=response.get('sql', draft.sql),
            intent=response.get('intent', draft.intent),
            entities=['InventoryItem'],
            filters=response.get('filters', draft.filters),
            reasoning=response.get('reasoning', draft.reasoning)
        )
    
    def _generate_with_keywords(self, natural_language_query: str) -> DraftQuery:
        """Fallback keyword-based generation (used when GPT is unavailable)."""
        query = natural_language_query.lower().strip()
        
        filters: Dict[str, Any] = {}
        
        # Extract filters from query first
        if 'electronics' in query or 'electronic' in query:
            filters['category'] = 'Electronics'
        elif 'clothing' in query or 'clothes' in query or 'apparel' in query:
            filters['category'] = 'Clothing'
        elif 'home' in query or 'garden' in query:
            filters['category'] = 'Home & Garden'
        
        if 'last 30 days' in query or '30 days' in query:
            filters['timeRange'] = '30 days'
        
        # Detect intent and generate SQL
        if 'top' in query or 'best' in query or 'selling' in query:
            intent = 'top_sellers'
            sql = self._generate_top_sellers_query(query, filters)
        elif 'low stock' in query or 'out of stock' in query or 'reorder' in query:
            intent = 'low_stock'
            sql = self._generate_low_stock_query(query, filters)
        elif 'show' in query or 'list' in query or 'find' in query:
            intent = 'list_items'
            sql = self._generate_list_query(query, filters)
        else:
            intent = 'list_items'
            sql = self._generate_list_query(query, filters)
        
        return DraftQuery(
            sql=sql,
            intent=intent,
            entities=['InventoryItem'],
            filters=filters,
            reasoning='Generated using keyword-based fallback'
        )
    
    def _generate_top_sellers_query(self, query: str, filters: Dict[str, Any]) -> str:
        """Generate top sellers query."""
        limit = self._extract_limit(query) or 10
        where_clauses = ['i.recent_sales_volume > 0']
        
        if 'category' in filters:
            where_clauses.append(f"c.name = '{filters['category']}'")
        
        where_clause = ' AND '.join(where_clauses)
        
        return f"""
            SELECT 
                i.id,
                i.sku,
                i.name,
                i.category_id as categoryId,
                i.location_id as locationId,
                i.current_stock as currentStock,
                i.reorder_threshold as reorderThreshold,
                i.recent_sales_volume as recentSalesVolume,
                i.created_at as createdAt,
                i.updated_at as updatedAt
            FROM inventory_items i
            LEFT JOIN product_categories c ON i.category_id = c.id
            WHERE {where_clause}
            ORDER BY i.recent_sales_volume DESC
            LIMIT {limit}
        """.strip()
    
    def _generate_low_stock_query(self, query: str, filters: Dict[str, Any]) -> str:
        """Generate low stock query."""
        where_clauses = ['i.current_stock <= i.reorder_threshold']
        
        if 'category' in filters:
            where_clauses.append(f"c.name = '{filters['category']}'")
        
        where_clause = ' AND '.join(where_clauses)
        
        return f"""
            SELECT 
                i.id,
                i.sku,
                i.name,
                i.category_id as categoryId,
                i.location_id as locationId,
                i.current_stock as currentStock,
                i.reorder_threshold as reorderThreshold,
                i.recent_sales_volume as recentSalesVolume,
                i.created_at as createdAt,
                i.updated_at as updatedAt
            FROM inventory_items i
            LEFT JOIN product_categories c ON i.category_id = c.id
            WHERE {where_clause}
            ORDER BY i.current_stock ASC, i.recent_sales_volume DESC
            LIMIT 100
        """.strip()
    
    def _generate_list_query(self, query: str, filters: Dict[str, Any]) -> str:
        """Generate list query."""
        limit = self._extract_limit(query) or 50
        where_clauses = []
        
        if 'category' in filters:
            where_clauses.append(f"c.name = '{filters['category']}'")
        
        where_clause = f"WHERE {' AND '.join(where_clauses)}" if where_clauses else ''
        
        return f"""
            SELECT 
                i.id,
                i.sku,
                i.name,
                i.category_id as categoryId,
                i.location_id as locationId,
                i.current_stock as currentStock,
                i.reorder_threshold as reorderThreshold,
                i.recent_sales_volume as recentSalesVolume,
                i.created_at as createdAt,
                i.updated_at as updatedAt
            FROM inventory_items i
            LEFT JOIN product_categories c ON i.category_id = c.id
            {where_clause}
            ORDER BY i.updated_at DESC
            LIMIT {limit}
        """.strip()
    
    def _extract_limit(self, query: str) -> Optional[int]:
        """Extract limit number from query."""
        match = re.search(r'(\d+)', query)
        return int(match.group(1)) if match else None


# Global instance
nl_query_draft_service = NLQueryDraftService()

