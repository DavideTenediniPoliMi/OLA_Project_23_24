from abc import ABC

from logger.logger import Logger


class Agent(ABC):
    def __init__(self) -> None:
        Logger.info(f"This simulation is using a {self.__class__}")
