"""Configuration management for the backend."""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration."""
    
    # Server Configuration
    PORT = int(os.getenv('PORT', '3001'))
    NODE_ENV = os.getenv('NODE_ENV', 'development')
    
    # Database Configuration
    DB_PATH = os.getenv('DB_PATH', 'inventory.db')
    
    # CORS Configuration
    CORS_ORIGIN = os.getenv('CORS_ORIGIN', 'http://localhost:3000')
    
    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'info')
    
    # OpenAI Configuration
    class OpenAI:
        # Azure OpenAI Configuration
        API_KEY = os.getenv('AZURE_OPENAI_API_KEY') or os.getenv('OPENAI_API_KEY', '')
        ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT', '')
        DEPLOYMENT = os.getenv('AZURE_OPENAI_DEPLOYMENT', 'gpt-4o')
        API_VERSION = os.getenv('AZURE_OPENAI_API_VERSION', '2025-01-01-preview')
        
        # Standard OpenAI Configuration (fallback)
        MODEL = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
        
        # Enable/disable
        ENABLED = os.getenv('OPENAI_ENABLED', 'true').lower() != 'false'
        
        # Determine if using Azure
        IS_AZURE = bool(os.getenv('AZURE_OPENAI_ENDPOINT'))
    
    openai = OpenAI()

config = Config()

