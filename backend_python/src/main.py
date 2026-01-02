"""Main entry point for the Python backend."""
import sys
import time
import uvicorn
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from services.db.connection import test_connection, get_database
from services.logging.logger import logger_instance as logger
from api import create_app
from config import config


def main():
    """Main function to start the server."""
    logger.info('Starting Natural Language Inventory Dashboard backend...')
    
    # Test database connection (with retry)
    db_connected = False
    retries = 3
    
    while not db_connected and retries > 0:
        db_connected = test_connection()
        if not db_connected:
            retries -= 1
            if retries > 0:
                logger.warn(f'Database connection failed, retrying... ({retries} attempts left)')
                time.sleep(2)
    
    if not db_connected:
        logger.error('Database connection failed after retries - cannot start server')
        logger.error('Please check the error messages above for details')
        return
    
    logger.info('Database connection successful')
    
    # Create FastAPI app
    app = create_app()
    
    # Start server
    logger.info(f'Server listening on port {config.PORT}')
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=config.PORT,
        log_level=config.LOG_LEVEL.lower()
    )


if __name__ == "__main__":
    main()

