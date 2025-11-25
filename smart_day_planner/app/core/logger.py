import logging
import os
from datetime import datetime

def setup_logger():
    """Setup application logger"""
    
    os.makedirs("logs", exist_ok=True)
    
    logger = logging.getLogger("smart_day_planner")
    logger.setLevel(logging.DEBUG)
    
    detailed_formatter = logging.Formatter(
        '[%(levelname)s] %(asctime)s - %(name)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    simple_formatter = logging.Formatter(
        '[%(levelname)s] %(asctime)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    log_file = os.path.join("logs", f"app_{datetime.now().strftime('%Y%m%d')}.log")
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(detailed_formatter)
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(simple_formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    logger.info("="*50)
    logger.info("Smart Day Planner Logger Initialized")
    logger.info("="*50)
    
    return logger

def get_logger():
    """Get existing logger instance"""
    return logging.getLogger("smart_day_planner")