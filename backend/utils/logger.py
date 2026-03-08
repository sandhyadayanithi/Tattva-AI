import logging
import sys

def setup_logger(name="tattva_ai"):
    """Configures a shared logger for the project."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Create console handler with a nice format
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )
    handler.setFormatter(formatter)
    
    if not logger.handlers:
        logger.addHandler(handler)
        
    return logger

# Global logger instance
logger = setup_logger()
