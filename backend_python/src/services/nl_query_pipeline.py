"""NL Query Pipeline - orchestrates the full NL→query flow."""
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.nl_query_draft_service import nl_query_draft_service
from services.inventory_query_executor import inventory_query_executor
from models.inventory_query_session import InventoryQuerySession, QuerySessionStatus
from services.logging.logger import logger_instance as logger


class PipelineResult:
    """Pipeline result model."""
    def __init__(self, session: InventoryQuerySession, 
                 results: Optional[Dict[str, Any]] = None):
        self.session = session
        self.results = results


class NLQueryPipeline:
    """Execute the full NL→query pipeline: draft → review → execute."""
    
    async def process_query(self, natural_language_query: str, user_id: str,
                          session_id: str) -> PipelineResult:
        """Process a natural language query through the full pipeline.
        
        For User Story 1, we skip the review step (will be added in User Story 2)
        """
        logger.info('Processing NL query', {
            'sessionId': session_id,
            'userId': user_id,
            'query': natural_language_query
        })
        
        # Step 1: Draft generation
        draft = await nl_query_draft_service.generate_draft(natural_language_query)
        
        session = InventoryQuerySession(
            id=session_id,
            userId=user_id,
            naturalLanguageQuery=natural_language_query,
            draftQuery=draft.sql,
            status=QuerySessionStatus.DRAFTED,
            createdAt=datetime.now(),
            updatedAt=datetime.now()
        )
        
        # Step 2: Self-review (simplified for US1, will be enhanced in US2)
        # For now, we'll execute directly if the query looks safe
        session.status = QuerySessionStatus.EXECUTING
        session.updatedAt = datetime.now()
        
        try:
            # Step 3: Execute
            result = await inventory_query_executor.execute_query(draft.sql)
            
            session.status = QuerySessionStatus.EXECUTED
            session.finalQuery = draft.sql
            session.executedAt = datetime.now()
            session.resultSummary = {
                'rowCount': result.row_count,
                'keyAggregates': {},
            }
            session.updatedAt = datetime.now()
            
            logger.info('Query pipeline completed successfully', {
                'sessionId': session_id,
                'rowCount': result.row_count,
            })
            
            return PipelineResult(
                session=session,
                results={
                    'rows': result.rows,
                    'rowCount': result.row_count,
                    'executionTimeMs': result.execution_time_ms,
                }
            )
        except Exception as e:
            session.status = QuerySessionStatus.FAILED
            session.updatedAt = datetime.now()
            logger.error('Query pipeline failed', {
                'sessionId': session_id,
                'error': str(e),
            })
            raise


# Global instance
nl_query_pipeline = NLQueryPipeline()

