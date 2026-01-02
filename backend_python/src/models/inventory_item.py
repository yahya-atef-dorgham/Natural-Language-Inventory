"""Inventory item model."""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class InventoryItem(BaseModel):
    """Inventory item model."""
    id: str
    sku: str
    name: str
    categoryId: Optional[str] = None
    locationId: Optional[str] = None
    currentStock: int = 0
    reorderThreshold: int = 0
    recentSalesVolume: int = 0
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None
    
    class Config:
        """Pydantic config."""
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }

