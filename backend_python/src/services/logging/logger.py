"""Logging service for the application."""
import logging
import sys
import os
from typing import Any, Dict
from pathlib import Path

# Add src to path for imports
_src_path = Path(__file__).parent.parent.parent
if str(_src_path) not in sys.path:
    sys.path.insert(0, str(_src_path))

try:
    from config import config
    _log_level = getattr(logging, config.LOG_LEVEL.upper(), logging.INFO)
except ImportError:
    _log_level = logging.INFO

# Configure logging
logging.basicConfig(
    level=_log_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger('nl-inventory-dashboard')

def log_info(message: str, context: Dict[str, Any] = None):
    """Log info message with optional context."""
    if context:
        logger.info(f"{message} | Context: {context}")
    else:
        logger.info(message)

def log_error(message: str, context: Dict[str, Any] = None):
    """Log error message with optional context."""
    if context:
        logger.error(f"{message} | Context: {context}")
    else:
        logger.error(message)

def log_warn(message: str, context: Dict[str, Any] = None):
    """Log warning message with optional context."""
    if context:
        logger.warning(f"{message} | Context: {context}")
    else:
        logger.warning(message)

# Export logger object for compatibility
class Logger:
    """Logger wrapper for compatibility with TypeScript-style logging."""
    
    def info(self, message: str, context: Dict[str, Any] = None):
        log_info(message, context)
    
    def error(self, message: str, context: Dict[str, Any] = None):
        log_error(message, context)
    
    def warn(self, message: str, context: Dict[str, Any] = None):
        log_warn(message, context)
    
    def warning(self, message: str, context: Dict[str, Any] = None):
        log_warn(message, context)

logger_instance = Logger()

