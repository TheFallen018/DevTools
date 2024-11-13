import inspect
import logging
import os
import threading
import typing
from ctypes import *
from ctypes import wintypes
from datetime import datetime
from typing import Tuple, Any

COLORS = {
    'red': '\033[91m',
    'green': '\033[92m',
    'yellow': '\033[93m',
    'blue': '\033[94m',
    'magenta': '\033[95m',
    'cyan': '\033[96m',
    'reset': '\033[0m'
}

# Custom log levels
CUSTOM_LOG_LEVELS = {
    'INFO': 25,
    'SUCCESS': 25,
    'DEBUG': 15,
    'WARNING': 30,
    'ERROR': 40,
    'CRITICAL': 50
}

LOG_LEVEL_RETURN_CODES = {
    'SUCCESS': 1,
    'INFO': 0,
    'DEBUG': 0,
    'WARNING': -1,
    'ERROR': -2,
    'CRITICAL': -3
}


class PROCESSOR_NUMBER(Structure):
    _fields_ = [("Group", wintypes.WORD),
                ("Number", wintypes.BYTE),
                ("Reserved", wintypes.BYTE)]


PN = PROCESSOR_NUMBER()


class LOGGER_SETTINGS():
    def __init__(self):
        self.log_level = 'INFO'
        self.show_core = False
        self.show_thread = False
        self.show_time = False


LS = LOGGER_SETTINGS()


def log(message: Any, level: str = 'DEBUG', color: str = None, flush: bool = False, silent: bool = False) -> Tuple[
    Any, str]:
    custom_level = level

    # Get log level name and value
    level_name = level.upper()
    level_value = CUSTOM_LOG_LEVELS.get(level_name, logging.INFO)

    # Check if the log level is enabled
    if level_value < logging.getLogger().getEffectiveLevel():
        return None, ""

    message = str(message)

    # Get core number
    windll.kernel32.GetCurrentProcessorNumberEx(byref(PN))
    core = PN.Number

    # Get thread ID
    thread_id = threading.get_ident()

    # Get log level name and value
    level_name = level.upper()
    level_value = CUSTOM_LOG_LEVELS.get(level_name, logging.INFO)

    # Format log message
    formatted_message = ""
    if LS.show_core:
        formatted_message = f"[Core: {core}]"
    if LS.show_thread:
        formatted_message = f"{formatted_message}[Thread {thread_id}:]"
    if LS.show_time:
        formatted_message = f"{formatted_message}[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]"

    # Use inspect to get caller information
    frame = inspect.currentframe().f_back
    caller_filename = os.path.basename(frame.f_code.co_filename)
    caller_lineno = frame.f_lineno

    formatted_message = f"{formatted_message}[{level_name}][{caller_filename}:{caller_lineno}]: {message}"

    # Apply color if specified and valid
    if color and color.lower() in COLORS:
        formatted_message = f"{COLORS[color.lower()]}{formatted_message}{COLORS['reset']}"

    # Check if the log level is enabled
    if level_value >= logging.getLogger().getEffectiveLevel():
        # Print the formatted log message
        print(formatted_message, flush=flush)

    return LOG_LEVEL_RETURN_CODES[custom_level.upper()], formatted_message


def set_log_level(level: str = 'INFO', show_core=False, show_thread=False, show_time=False) -> None:
    """
    Sets the logging level for the logger.

    Args:
        level (str, optional): The log level ('INFO', 'DEBUG', 'WARNING', 'ERROR', 'CRITICAL'). Defaults to 'INFO'.

    Returns:
        None
    """
    LS.show_core = show_core
    LS.show_thread = show_thread
    LS.show_time = show_time
    logging.getLogger().setLevel(CUSTOM_LOG_LEVELS.get(level.upper(), logging.INFO))
