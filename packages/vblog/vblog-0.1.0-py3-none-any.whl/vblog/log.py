#!/usr/bin/env python3
from dataclasses import dataclass
import enum
import logging, logging.config
import os
import sys
import pathlib
from typing import List


class LogColors(enum.Enum):
    RED = "\033[0;31m"
    RED_BOLD = "\033[1;31m"
    GREEN = "\033[0;32m"
    GREEN_BOLD = "\033[1;32m"
    YELLOW = "\033[0;33m"
    YELLOW_BOLD = "\033[1;33m"
    BLUE = "\033[0;34m"
    BLUE_BOLD = "\033[1;34m"
    MAGENTA = "\033[0;35m"
    MAGENTA_BOLD = "\033[1;35m"
    CYAN = "\033[0;36m"
    CYAN_BOLD = "\033[1;36m"
    WHITE = "\033[0;37m"
    WHITE_BOLD = "\033[1;37m"
    GREY = "\033[0;38m"
    GREY_BOLD = "\033[1;38m"
    NONE = "\033[0m"


class StreamHandlerFormatter(logging.Formatter):
    """Custom stream handler (use colors)"""

    def __init__(self, fmt):
        super().__init__()
        self.fmt = fmt
        self.formats = {
            logging.DEBUG: LogColors.MAGENTA.value + self.fmt + LogColors.NONE.value,
            logging.INFO: LogColors.GREY.value + self.fmt + LogColors.NONE.value,
            25 : LogColors.GREEN.value + self.fmt + LogColors.NONE.value,
            logging.WARNING: LogColors.YELLOW.value + self.fmt + LogColors.NONE.value,
            logging.ERROR: LogColors.RED.value + self.fmt + LogColors.NONE.value,
            logging.CRITICAL: LogColors.RED_BOLD.value + self.fmt + LogColors.NONE.value,
        }

    def format(self, record):
        log_fmt = self.fmt
        if record.levelno in self.formats:
            log_fmt = self.formats.get(record.levelno)
        formatter = logging.Formatter(log_fmt)

        return formatter.format(record)


@dataclass
class Logger:
    """Custom Logger"""

    log_configuration_path: str = "" #@TODO default value from config

    def __post_init__(self):
        # Check if configuration file exists
        if self.log_configuration_path:
            conf = pathlib.Path(self.log_configuration_path).resolve()
            if conf.exists():
                self.log_configuration_path = str(conf)
            else:
                print(f"configuration not found in '{self.log_configuration_path}'")
                self.log_configuration_path = ""

        # Load default configuration if needed
        if not self.log_configuration_path:
            conf = pathlib.Path(f"{os.path.dirname(__file__)}/default_logger.cfg").resolve()
            if conf.exists():
                self.log_configuration_path = str(conf)

        if self.log_configuration_path:
            logging.addLevelName(25, "OK")
            # Load configuration
            logging.config.fileConfig(self.log_configuration_path)
            self._logger = logging.getLogger("default")

            # Format the logger handlers
            for handler in self._logger.handlers:
                if isinstance(handler, logging.FileHandler):
                    pass
                elif isinstance(handler, logging.StreamHandler) and handler.formatter:
                    handler.setFormatter(StreamHandlerFormatter(handler.formatter._fmt))

            self._logger.debug(f"LAUNCH : {sys.argv}")
        else:
            exit()

    def get_streamHandlers(self):
        handlers: List[logging.StreamHandler] = []
        for handler in self._logger.handlers:
            if isinstance(handler, logging.FileHandler):
                pass
            elif isinstance(handler, logging.StreamHandler):
                handlers.append(handler)

        return handlers

    def get_fileHandlers(self):
        handlers: List[logging.FileHandler] = []
        for handler in self._logger.handlers:
            if isinstance(handler, logging.FileHandler):
                handlers.append(handler)

        return handlers

    def set_stream_handlers_level(self, level: int):
        for handler in self._logger.handlers:
            if isinstance(handler, logging.FileHandler):
                pass
            elif isinstance(handler, logging.StreamHandler):
                handler.setLevel(level)

    def debug(self, message: str, *args, **kws):
        self._logger._log(logging.DEBUG, message, args, **kws)

    def info(self, message: str, *args, **kws):
        self._logger._log(logging.INFO, message, args, **kws)

    def ok(self, message : str, *args, **kws):
        self._logger._log(25, message, args, **kws)

    def warning(self, message: str, *args, **kws):
        self._logger._log(logging.WARNING, message, args, **kws)

    def error(self, message: str, *args, **kws):
        self._logger._log(logging.ERROR, message, args, **kws)

    def critical(self, message: str, *args, **kws):
        self._logger._log(logging.CRITICAL, message, args, **kws)
