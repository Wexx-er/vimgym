"""
VimGym custom exceptions and error handling.
"""

from typing import Optional, Any


class VimGymError(Exception):
    """Base exception for all VimGym errors."""
    
    def __init__(self, message: str, details: Optional[Any] = None):
        super().__init__(message)
        self.message = message
        self.details = details


class ModuleError(VimGymError):
    """Errors related to learning modules."""
    pass


class LessonError(VimGymError):
    """Errors related to lessons."""
    pass


class ExerciseError(VimGymError):
    """Errors related to exercises."""
    pass


class SimulatorError(VimGymError):
    """Errors related to the Vim simulator."""
    pass


class ProgressError(VimGymError):
    """Errors related to progress tracking."""
    pass


class DatabaseError(VimGymError):
    """Errors related to data storage."""
    pass


class UserError(VimGymError):
    """Errors related to user management."""
    pass


class ConfigurationError(VimGymError):
    """Errors related to configuration."""
    pass


class ValidationError(VimGymError):
    """Errors related to data validation."""
    pass


def handle_error(logger, error: Exception, context: str = "") -> None:
    """Handle and log errors consistently."""
    error_msg = f"{context}: {str(error)}" if context else str(error)
    
    if isinstance(error, VimGymError):
        logger.error(f"VimGym Error - {error_msg}")
        if error.details:
            logger.debug(f"Error details: {error.details}")
    else:
        logger.error(f"Unexpected Error - {error_msg}")
        logger.exception("Full traceback:")


def safe_execute(func, logger, context: str = "", default_return=None):
    """Safely execute a function with error handling."""
    try:
        return func()
    except Exception as e:
        handle_error(logger, e, context)
        return default_return