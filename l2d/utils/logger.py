import logging
import os

from rich.logging import RichHandler


class LogFilter(logging.Filter):
    """
    Print all messages that do not include "dealloc" (GPU warning message).
    """

    def filter(self, record: logging.LogRecord):
        # Put the filter logic here to not print out certain messages
        # if "dealloc" in str(getattr(record, "msg")):
        #     return False
        return True

    def __repr__(self):
        return "LogFilter"


def create_logger(name: str) -> logging.Logger:
    """Create a `Logger` to be used in different modules

    Arguments:
        name: The name of the logger. Will usually be passed in from the module as `__name__`.

    Returns:
        The `Logger` object that will be used to create log statements in the terminal.
    """
    if (log_level := os.environ.get("LOGLEVEL")) is None:
        log_level = "INFO"

    FORMAT = "%(message)s"
    rh = RichHandler()
    rh.addFilter(LogFilter())
    handlers = [rh]
    logging.basicConfig(
        level=log_level,
        format=FORMAT,
        datefmt="[%m/%d/%Y %I:%M:%S %p]",
        handlers=handlers,
    )

    log = logging.getLogger(name)
    log.setLevel(log_level)

    return log
