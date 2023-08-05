#!/usr/bin/env python3
from datetime import datetime
from pathlib import Path
import re
import logging
from log import Logger

LOGGER = Logger()


class LogParser:
    def __init__(self, logfile_path: str):
        self.logfile_path: str = logfile_path
        self.logs = []

    def is_logfile_exists(self):
        """is logfile existing

        Returns:
            bool: file exist
        """
        return Path(self.logfile_path).exists()

    def logfile_exists(self):
        """check if logfile exists"""
        if not self.is_logfile_exists():
            LOGGER.error(f"'{self.logfile_path}' not found")
            exit()

    def dump(self):
        """dump logfile"""
        Path(self.logfile_path).unlink(missing_ok=True)

    @staticmethod
    def _string_to_LogRecord(string: str, file_handler: logging.FileHandler, regex: str):

        found = re.search(regex, string)
        if file_handler.formatter:
            date_fmt = (
                file_handler.formatter.default_time_format
                if file_handler.formatter.datefmt == ""
                else file_handler.formatter.datefmt
            )
            date_fmt += (
                ",%f" if file_handler.formatter.default_msec_format else ""
            )  # @TODO nok le %f pas vraiment exacte

            if found and len(found.groups()) == 5:
                log = logging.LogRecord(
                    name="",
                    level=logging.getLevelName(found.group(2)),
                    pathname=found.group(3),
                    lineno=int(found.group(4)),
                    msg=found.group(5),
                    args=None,
                    exc_info=None,
                )

                t = datetime.strptime(found.group(1), date_fmt)  # type: ignore
                log.created = t.timestamp()

                return log

    def load(self, file_handler: logging.FileHandler, regex: str):
        self.logfile_exists()
        logfile = open(self.logfile_path, "r")
        logfile_lines = logfile.readlines()

        # Check if regex is valid with this FileHandler
        log_sample = file_handler.format(logging.LogRecord("name", logging.INFO, "pathname", 0, "message", None, None))
        check = re.search(regex, log_sample)

        if check is None or len(check.groups()) != 5:
            LOGGER.error(
                f"regex specified '{regex}' is not valid for FileHandler '{file_handler.name}' for '{self.logfile_path}'"
            )
            exit()

        # Build LogRecord
        self.logs = []
        for i in range(len(logfile_lines)):
            log = self._string_to_LogRecord(
                logfile_lines[i],
                file_handler,
                regex,
            )

            # format the log correctly (avoid line breaking)
            if isinstance(log, logging.LogRecord):
                self.logs.append(log)
            else:
                if len(self.logs) > 0:
                    last = self.logs.pop()
                    if isinstance(last, logging.LogRecord):
                        last.msg += f"\n{logfile_lines[i]}"
                        self.logs.append(last)

    def stdout(self, stream_handler: logging.StreamHandler):
        """print log to stdout

        Args:
            stream_handler (logging.StreamHandler) : stream handler to use convert logs
        """
        index = 0

        for log in self.logs:
            index += 1
            if isinstance(log, logging.LogRecord):
                print(f"{str(index).ljust(5)}{stream_handler.format(log)}")
