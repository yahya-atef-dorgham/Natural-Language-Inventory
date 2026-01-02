"""Authentication middleware."""
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel


class User(BaseModel):
    """User model."""
    id: str
    role: str


security = HTTPBearer()


async def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)) -> User:
    """Get current user from token (mock implementation)."""
    # Mock authentication - in production, validate JWT token
    token = credentials.credentials
    
    if token == 'mock-token':
        return User(id='user-1', role='Admin')
    
    raise HTTPException(status_code=401, detail="Invalid authentication credentials")

