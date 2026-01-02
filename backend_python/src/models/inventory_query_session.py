"""Inventory query session model."""
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum
from pydantic import BaseModel


class QuerySessionStatus(str, Enum):
    """Query session status enum."""
    DRAFTED = 'drafted'
    REVIEWING = 'reviewing'
    REJECTED = 'rejected'
    EXECUTING = 'executing'
    EXECUTED = 'executed'
    FAILED = 'failed'


class ReviewFindings(BaseModel):
    """Review findings model."""
    flags: List[str] = []
    adjustments: List[str] = []
    defaultsApplied: List[str] = []
    safetyChecks: Dict[str, bool] = {
        'isReadOnly': True,
        'hasRowLimit': False,
        'hasTimeFilter': False,
    }


class InventoryQuerySession(BaseModel):
    """Inventory query session model."""
    id: str
    userId: str
    naturalLanguageQuery: str
    draftQuery: Optional[str] = None
    reviewFindings: Optional[ReviewFindings] = None
    finalQuery: Optional[str] = None
    status: QuerySessionStatus
    executedAt: Optional[datetime] = None
    resultSummary: Optional[Dict[str, Any]] = None
    createdAt: datetime
    updatedAt: datetime
    
    class Config:
        """Pydantic config."""
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }

