#!/usr/bin/env python3

from log_parser import LogParser, LOGGER

if __name__ == "__main__":
    # log
    LOGGER.debug("debug log")
    LOGGER.info("info log")
    LOGGER.ok("ok log")
    LOGGER.warning("warning log")
    LOGGER.error("error log")
    LOGGER.critical("critical log")
    # log_parser
    file_handlers = LOGGER.get_fileHandlers()
    for file_handler in file_handlers:
        print(f"Parse logfile : '{file_handler.baseFilename}'")
        log_parser = LogParser(file_handler.baseFilename) #@TODO  parser  Logger plutot qu'individuel
        regex =  r"([\d-]+\s[\d:]+,[\d:]+)\s\[\s*([A-Z]+)\]\s*([A-Za-z]+.[A-Za-z]+):(\d+)\s*\|*(.*)" #@TODO conf
        log_parser.load(file_handler,regex)
        log_parser.stdout(LOGGER.get_streamHandlers()[0])
    