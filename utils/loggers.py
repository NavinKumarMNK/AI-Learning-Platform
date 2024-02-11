import logging
from abc import ABC

from utils.parsers import DictObjectParser

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

    def info(self, msg: str, *args, **kwargs) -> None:
        self.logger.info(msg, *args, **kwargs)


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

        self.handler.setLevel(logging.INFO)
        self.logger.addHandler(self.handler)


class FileLogger(Logger):
    """File logger for logging to file"""

    def __init__(self, name: str, filename: str, mode="w"):
        super().__init__(name)
        self.handler = logging.FileHandler(filename, mode=mode)
        self.handler.setLevel(logging.INFO)

        self.handler.setFormatter(
            logging.Formatter(
                "[%(asctime)s T%(thread).5s P%(process)s %(levelname)7s %(name)s:%(lineno)s] %(message)s"
            )
        )

        self.logger.addHandler(self.handler)


def load_loggers(config: DictObjectParser):
    if config.console:
        ConsoleLogger(name=__name__, rich=config.console.rich)
    if config.file:
        FileLogger(
            name=__name__,
            filename=config.file.filename,
            mode=config.file.mode,
        )

    logger = logging.getLogger(
        __name__,
    )
    return logger


if __name__ == "__main__":
    console_logger = ConsoleLogger(name="logger", rich=True)
    file_logger = FileLogger(name="logger", filename="./logs/test.log", mode="w")
    # console_logger = GroupLogger([console_logger, file_logger])
    logger = logging.getLogger(name="logger")
    logger.debug(msg="debug")
    logger.log(msg="log", level=1)
    logger.exception(msg="exception")
    logger.warning(msg="warning")
    logger.error(msg="error")
    logger.critical(msg="critical")

    # log the error itself not the handled exception
    try:
        raise Exception("test")
    except Exception as e:
        logger.exception("exception", exc_info=e)
