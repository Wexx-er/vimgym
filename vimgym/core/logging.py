"""
Logging configuration for VimGym.
"""

import logging
import sys
from pathlib import Path
from typing import Optional
from datetime import datetime

from rich.console import Console
from rich.logging import RichHandler


class VimGymLogger:
    """Centralized logging for VimGym application."""
    
    def __init__(self, 
                 data_dir: Optional[Path] = None,
                 debug_mode: bool = False,
                 console: Optional[Console] = None):
        self.data_dir = data_dir
        self.debug_mode = debug_mode
        self.console = console or Console()
        self.logger = self._setup_logger()
    
    def _setup_logger(self) -> logging.Logger:
        """Set up logger with appropriate handlers."""
        logger = logging.getLogger('vimgym')
        
        # Clear existing handlers
        logger.handlers.clear()
        
        # Set level
        if self.debug_mode:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)
        
        # Console handler with Rich formatting
        console_handler = RichHandler(
            console=self.console,
            show_time=False,
            show_path=False,
            markup=True
        )
        console_handler.setLevel(logging.WARNING)  # Only warnings and errors to console
        
        # Custom format for console
        console_format = logging.Formatter(
            "[%(levelname)s] %(message)s"
        )
        console_handler.setFormatter(console_format)
        logger.addHandler(console_handler)
        
        # File handler if data directory is available
        if self.data_dir:
            try:
                log_file = self.data_dir / "vimgym.log"
                file_handler = logging.FileHandler(log_file, encoding='utf-8')
                
                if self.debug_mode:
                    file_handler.setLevel(logging.DEBUG)
                else:
                    file_handler.setLevel(logging.INFO)
                
                # Detailed format for file
                file_format = logging.Formatter(
                    "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s"
                )
                file_handler.setFormatter(file_format)
                logger.addHandler(file_handler)
                
                logger.info(f"Logging initialized. Log file: {log_file}")
                
            except Exception as e:
                logger.warning(f"Could not set up file logging: {e}")
        
        return logger
    
    def get_logger(self) -> logging.Logger:
        """Get the configured logger."""
        return self.logger


def setup_logging(data_dir: Optional[Path] = None, 
                 debug_mode: bool = False,
                 console: Optional[Console] = None) -> logging.Logger:
    """Set up VimGym logging and return the logger."""
    vim_logger = VimGymLogger(data_dir, debug_mode, console)
    return vim_logger.get_logger()