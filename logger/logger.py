import logging
import os
from datetime import datetime as dt
from typing import Optional, Self


class Logger:
    """Static utility class that provides an unified logging experience."""

    debugger: Optional[logging.Logger] = None
    infoer: Optional[logging.Logger] = None

    # Prevent instantiation
    def __new__(cls) -> Self:
        raise RuntimeError(f"{cls} should not be instantiated")

    @staticmethod
    def init(path_to_folder: str = "") -> None:
        Logger.path = path_to_folder

    @staticmethod
    def debug(*message: str) -> None:
        if Logger.debugger == None:
            Logger.debugger = Logger.lazy_init("my_debugger", logging.DEBUG)
        Logger.debugger.debug(" ".join([str(m) for m in message]))

    @staticmethod
    def info(*message) -> None:
        if Logger.infoer == None:
            Logger.infoer = Logger.lazy_init("my_infoer", logging.INFO)
        Logger.infoer.info(" ".join([str(m) for m in message]))

    @staticmethod
    def lazy_init(name, level) -> None:
        logger = logging.getLogger(name)
        logger.setLevel(level)

        fh = logging.FileHandler(
            Logger.path
            + name
            + "\\"
            + str(dt.now().strftime("%Y%m%d-%H%M%S"))
            + ".log"
        )
        fh.setLevel(level)
        logger.addHandler(fh)

        return logger

    @staticmethod
    def clear_logs(path: str) -> None:
        for folder in ["debug\\", "info\\"]:
            dir_name = path + folder
            items = os.listdir(dir_name)

            for item in items:
                if item.endswith(".log"):
                    os.remove(os.path.join(dir_name, item))
