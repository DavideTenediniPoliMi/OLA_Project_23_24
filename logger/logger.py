import logging
import os
from datetime import datetime as dt
from typing import Self


class Logger:
    """Static utility class that provides an unified logging experience."""

    debugger: logging.Logger
    infoer: logging.Logger

    # Prevent instantiation
    def __new__(cls) -> Self:
        raise RuntimeError(f"{cls} should not be instantiated")

    @staticmethod
    def init(path_to_folder: str = "") -> None:
        Logger.debugger = logging.getLogger("my_debugger")
        Logger.debugger.setLevel(logging.DEBUG)

        Logger.infoer = logging.getLogger("my_infoer")
        Logger.infoer.setLevel(logging.INFO)

        fh_debug = logging.FileHandler(
            path_to_folder
            + "debug\\"
            + str(dt.now().strftime("%Y%m%d-%H%M%S"))
            + ".log"
        )
        fh_debug.setLevel(logging.DEBUG)
        Logger.debugger.addHandler(fh_debug)

        fh_info = logging.FileHandler(
            path_to_folder
            + "info\\"
            + str(dt.now().strftime("%Y%m%d-%H%M%S"))
            + ".log"
        )
        fh_info.setLevel(logging.INFO)
        Logger.infoer.addHandler(fh_info)

    @staticmethod
    def debug(message: str) -> None:
        Logger.debugger.debug(message)

    @staticmethod
    def info(message: str) -> None:
        Logger.infoer.info(message)

    @staticmethod
    def clear_logs(path: str) -> None:
        for folder in ["debug\\", "info\\"]:
            dir_name = path + folder
            items = os.listdir(dir_name)

            for item in items:
                if item.endswith(".log"):
                    os.remove(os.path.join(dir_name, item))
