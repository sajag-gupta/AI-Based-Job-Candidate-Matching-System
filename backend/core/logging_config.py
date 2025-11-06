"""
Logging configuration with correlation IDs
"""
import logging
import sys
from contextvars import ContextVar
import uuid

# Context variable for correlation ID
correlation_id_var: ContextVar[str] = ContextVar('correlation_id', default='')


def get_correlation_id() -> str:
    """Get current correlation ID"""
    return correlation_id_var.get()


def set_correlation_id(correlation_id: str = None):
    """Set correlation ID for current context"""
    if correlation_id is None:
        correlation_id = str(uuid.uuid4())
    correlation_id_var.set(correlation_id)
    return correlation_id


class CorrelationIdFilter(logging.Filter):
    """Add correlation ID to log records"""
    
    def filter(self, record):
        record.correlation_id = get_correlation_id()
        return True


def setup_logging(log_level: str = "INFO"):
    """
    Setup logging configuration
    """
    log_format = (
        '%(asctime)s - %(name)s - %(levelname)s - '
        '[%(correlation_id)s] - %(message)s'
    )
    
    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format=log_format,
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Add correlation ID filter to all handlers
    for handler in logging.root.handlers:
        handler.addFilter(CorrelationIdFilter())
    
    # Reduce noise from third-party libraries
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
