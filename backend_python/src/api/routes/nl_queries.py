"""NL Queries API routes."""
import os
import sys
import uuid
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from api.middleware.auth_middleware import get_current_user, User
from services.nl_query_pipeline import nl_query_pipeline
from services.logging.logger import logger_instance as logger

router = APIRouter()

# In-memory session store (replace with database in production)
sessions: Dict[str, Any] = {}


class NLQueryRequest(BaseModel):
    """NL Query request model."""
    query: str
    context: Optional[Dict[str, Any]] = None


@router.post("/nl-queries")
async def submit_nl_query(
    request: NLQueryRequest,
    current_user: User = Depends(get_current_user)
):
    """Submit a natural language query."""
    try:
        if not request.query or not isinstance(request.query, str):
            raise HTTPException(
                status_code=400,
                detail={'error': 'Bad Request', 'message': 'Missing or invalid "query" field'}
            )
        
        session_id = str(uuid.uuid4())
        logger.info('Creating NL query session', {
            'sessionId': session_id,
            'userId': current_user.id
        })
        
        # Process query through pipeline
        result = await nl_query_pipeline.process_query(
            request.query,
            current_user.id,
            session_id
        )
        
        # Store session
        sessions[session_id] = result.session.dict()
        
        return {
            'sessionId': result.session.id,
            'status': result.session.status.value,
            'message': 'Query accepted and executing',
        }
    except Exception as e:
        error_message = str(e)
        logger.error('Error processing NL query', {
            'error': error_message,
            'query': request.query,
            'userId': current_user.id,
        })
        
        # Provide more helpful error messages
        status_code = 500
        user_message = 'Failed to process query'
        
        if 'forbidden keyword' in error_message or 'Only SELECT' in error_message:
            status_code = 400
            user_message = 'Query contains unsafe operations. Only read-only queries are allowed.'
        elif 'connect' in error_message or 'database' in error_message:
            status_code = 503
            user_message = 'Database temporarily unavailable. Please try again later.'
        elif 'not initialized' in error_message:
            status_code = 503
            user_message = 'Database not initialized. Please restart the server.'
        
        raise HTTPException(
            status_code=status_code,
            detail={
                'error': 'Bad Request' if status_code == 400 else 
                        'Service Unavailable' if status_code == 503 else 
                        'Internal Server Error',
                'message': user_message,
                'details': error_message if os.getenv('NODE_ENV') == 'development' else None
            }
        )


@router.get("/nl-queries/{session_id}")
async def get_query_results(
    session_id: str,
    current_user: User = Depends(get_current_user)
):
    """Retrieve query results."""
    try:
        session_data = sessions.get(session_id)
        
        if not session_data:
            raise HTTPException(
                status_code=404,
                detail={'error': 'Not Found', 'message': 'Session not found'}
            )
        
        # Check user access
        if session_data['userId'] != current_user.id and current_user.role != 'Admin':
            raise HTTPException(
                status_code=403,
                detail={'error': 'Forbidden', 'message': 'Access denied to this session'}
            )
        
        # Re-execute query to get fresh results (in production, cache results)
        result = await nl_query_pipeline.process_query(
            session_data['naturalLanguageQuery'],
            session_data['userId'],
            session_id
        )
        
        # Map results to API response format
        table_columns = []
        if result.results and result.results['rows'] and len(result.results['rows']) > 0:
            first_row = result.results['rows'][0]
            import re
            table_columns = [
                {
                    'id': key,
                    'label': key[0].upper() + re.sub(r'([A-Z])', r' \1', key[1:]),
                    'type': 'string',
                }
                for key in first_row.keys()
            ]
        
        # Generate multiple meaningful charts based on available data
        charts = []
        
        if result.results and result.results['rows']:
            rows = result.results['rows']
            
            # Chart 1: Stock Levels (Bar Chart)
            if any(r.get('currentStock') is not None for r in rows):
                charts.append({
                    'type': 'bar',
                    'title': 'Current Stock Levels',
                    'xAxisKey': 'name',
                    'data': sorted([
                        {
                            'name': (r.get('name') or r.get('sku') or 'Unknown')[:20],
                            'stock': r.get('currentStock', 0),
                            'threshold': r.get('reorderThreshold', 0),
                        }
                        for r in rows
                    ], key=lambda x: x['stock'], reverse=True)[:15],
                    'dataKeys': [
                        {'key': 'stock', 'name': 'Current Stock', 'color': '#6366f1'},
                        {'key': 'threshold', 'name': 'Reorder Threshold', 'color': '#ef4444'},
                    ],
                })
            
            # Chart 2: Sales Volume (Area Chart)
            if any(r.get('recentSalesVolume') is not None for r in rows):
                charts.append({
                    'type': 'area',
                    'title': 'Recent Sales Volume',
                    'xAxisKey': 'name',
                    'data': sorted([
                        {
                            'name': (r.get('name') or r.get('sku') or 'Unknown')[:20],
                            'sales': r.get('recentSalesVolume', 0),
                        }
                        for r in rows
                        if r.get('recentSalesVolume', 0) > 0
                    ], key=lambda x: x['sales'], reverse=True)[:15],
                    'dataKeys': [{'key': 'sales', 'name': 'Sales Volume', 'color': '#10b981'}],
                })
            
            # Chart 3: Stock vs Sales Comparison (Line Chart)
            if any(r.get('currentStock') is not None and r.get('recentSalesVolume') is not None for r in rows):
                max_stock = max((r.get('currentStock', 0) for r in rows), default=1)
                max_sales = max((r.get('recentSalesVolume', 0) for r in rows), default=1)
                scale_factor = max_stock / max_sales if max_sales > 0 else 1
                
                charts.append({
                    'type': 'line',
                    'title': 'Stock vs Sales Comparison',
                    'xAxisKey': 'name',
                    'data': sorted([
                        {
                            'name': (r.get('name') or r.get('sku') or 'Unknown')[:15],
                            'stock': r.get('currentStock', 0),
                            'sales': r.get('recentSalesVolume', 0) * scale_factor,
                            'salesOriginal': r.get('recentSalesVolume', 0),
                        }
                        for r in rows
                    ], key=lambda x: x['stock'], reverse=True)[:12],
                    'dataKeys': [
                        {'key': 'stock', 'name': 'Current Stock', 'color': '#6366f1'},
                        {'key': 'sales', 'name': 'Sales Volume (scaled)', 'color': '#10b981'},
                    ],
                })
            
            # Chart 4: Low Stock Alert
            low_stock_items = [
                r for r in rows
                if r.get('reorderThreshold', 0) > 0 and r.get('currentStock', 0) <= r.get('reorderThreshold', 0)
            ]
            
            if low_stock_items:
                charts.append({
                    'type': 'bar',
                    'title': 'Low Stock Alert - Items Below Reorder Threshold',
                    'xAxisKey': 'name',
                    'data': sorted([
                        {
                            'name': (r.get('name') or r.get('sku') or 'Unknown')[:20],
                            'stock': r.get('currentStock', 0),
                            'threshold': r.get('reorderThreshold', 0),
                            'deficit': max(0, r.get('reorderThreshold', 0) - r.get('currentStock', 0)),
                        }
                        for r in low_stock_items
                    ], key=lambda x: x['stock']),
                    'dataKeys': [
                        {'key': 'stock', 'name': 'Current Stock', 'color': '#ef4444'},
                        {'key': 'threshold', 'name': 'Reorder Threshold', 'color': '#f59e0b'},
                        {'key': 'deficit', 'name': 'Stock Deficit', 'color': '#dc2626'},
                    ],
                })
            
            # Chart 5: Top Performers Pie Chart
            if any(r.get('recentSalesVolume') is not None for r in rows):
                top_performers = sorted([
                    {
                        'name': (r.get('name') or r.get('sku') or 'Unknown')[:20],
                        'value': r.get('recentSalesVolume', 0),
                    }
                    for r in rows
                    if r.get('recentSalesVolume', 0) > 0
                ], key=lambda x: x['value'], reverse=True)[:8]
                
                if top_performers:
                    charts.append({
                        'type': 'pie',
                        'title': 'Top Selling Products Distribution',
                        'data': top_performers,
                        'dataKeys': [{'key': 'value', 'name': 'Sales Volume', 'color': '#6366f1'}],
                    })
            
            # Default chart if none created
            if not charts and rows:
                charts.append({
                    'type': 'bar',
                    'title': 'Inventory Overview',
                    'xAxisKey': 'name',
                    'data': [
                        {
                            'name': (r.get('name') or r.get('sku') or 'Unknown')[:20],
                            'value': r.get('currentStock') or r.get('recentSalesVolume') or 0,
                        }
                        for r in rows[:15]
                    ],
                    'dataKeys': [{'key': 'value', 'name': 'Value', 'color': '#6366f1'}],
                })
        
        return {
            'sessionId': result.session.id,
            'status': result.session.status.value,
            'reviewSummary': result.session.reviewFindings.dict() if result.session.reviewFindings else {},
            'table': {
                'columns': table_columns,
                'rows': result.results['rows'] if result.results else [],
            },
            'charts': charts,
            'message': 'Query executed successfully' if result.session.status.value == 'executed' else 'Query processing',
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error('Error retrieving query results', {'error': str(e)})
        raise HTTPException(
            status_code=500,
            detail={'error': 'Internal Server Error', 'message': 'Failed to retrieve results'}
        )


@router.get("/nl-queries")
async def list_sessions(current_user: User = Depends(get_current_user)):
    """List recent sessions."""
    try:
        # Filter sessions by user
        user_sessions = [
            {
                'sessionId': s['id'],
                'createdAt': s['createdAt'].isoformat() if isinstance(s['createdAt'], datetime) else s['createdAt'],
                'status': s['status'],
                'naturalLanguageQuery': s['naturalLanguageQuery'][:100],
            }
            for s in sessions.values()
            if s['userId'] == current_user.id
        ]
        
        user_sessions.sort(key=lambda x: x['createdAt'], reverse=True)
        
        return {'sessions': user_sessions[:20]}
    except Exception as e:
        logger.error('Error listing sessions', {'error': str(e)})
        raise HTTPException(
            status_code=500,
            detail={'error': 'Internal Server Error', 'message': 'Failed to list sessions'}
        )

