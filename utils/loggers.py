# author: entropy(NavinKumarMNK)
import logging
from abc import ABC

try:
    from rich.logging import RichHandler
    from rich.traceback import install

    RICH_LOGGING = True
except ImportError:
    RICH_LOGGING = False


class Logger(ABC):
    """Base logger class for logging"""

    def __init__(self, name: str) -> None:
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

    def debug(self, msg: str, *args, **kwargs) -> None:
        self.logger.debug(msg, *args, **kwargs)

    def log(self, msg: str, *args, **kwargs) -> None:
        self.logger.info(msg, *args, **kwargs)

    def exception(self, msg: str, *args, **kwargs) -> None:
        self.logger.exception(msg, *args, **kwargs)

    def warning(self, msg: str, *args, **kwargs) -> None:
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg: str, *args, **kwargs) -> None:
        self.logger.error(msg, *args, **kwargs)

    def critical(self, msg: str, *args, **kwargs) -> None:
        self.logger.critical(msg, *args, **kwargs)


class ConsoleLogger(Logger):
    """Console logger for logging to console"""

    def __init__(self, name: str, rich=True):
        super().__init__(name)
        if rich and RICH_LOGGING:
            self.handler = RichHandler(
                rich_tracebacks=True,
                show_time=True,
                show_level=True,
                show_path=True,
                markup=False,
            )
            install(show_locals=True)
        else:
            self.handler = logging.StreamHandler()

        self.handler.setLevel(logging.DEBUG)
        self.logger.addHandler(self.handler)


class FileLogger(Logger):
    """File logger for logging to file"""

    def __init__(self, name: str, filename: str, mode="w"):
        super().__init__(name)
        self.handler = logging.FileHandler(filename, mode=mode)
        self.handler.setLevel(logging.DEBUG)

        self.handler.setFormatter(
            logging.Formatter(
                "%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
            )
        )

        self.logger.addHandler(self.handler)


class GroupLogger:
    """Group logger for logging to multiple loggers at once"""

    def __init__(self, loggers: list = None):
        self.loggers = loggers

    def debug(self, msg: str, *args, **kwargs) -> None:
        for logger in self.loggers:
            logger.debug(msg, *args, **kwargs)

    def log(self, msg: str, *args, **kwargs) -> None:
        for logger in self.loggers:
            logger.log(msg, *args, **kwargs)

    def exception(self, msg: str, *args, **kwargs) -> None:
        for logger in self.loggers:
            logger.exception(msg, *args, **kwargs)

    def warning(self, msg: str, *args, **kwargs) -> None:
        for logger in self.loggers:
            logger.warning(msg, *args, **kwargs)

    def error(self, msg: str, *args, **kwargs) -> None:
        for logger in self.loggers:
            logger.error(msg, *args, **kwargs)

    def critical(self, msg: str, *args, **kwargs) -> None:
        for logger in self.loggers:
            logger.critical(msg, *args, **kwargs)


if __name__ == "__main__":
    console_logger = ConsoleLogger("consolelogger", rich=True)
    file_logger = FileLogger("filelogger", "test.log", mode="w")
    group_logger = GroupLogger([console_logger, file_logger])

    group_logger.debug("debug")
    group_logger.log("log")
    group_logger.exception("exception")
    group_logger.warning("warning")
    group_logger.error("error")
    group_logger.critical("critical")

    # log the error itself not the handled exception
    try:
        raise Exception("test")
    except Exception as e:
        group_logger.exception("exception", exc_info=e)
