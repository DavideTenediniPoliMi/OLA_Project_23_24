from abc import ABC

from logger.logger import Logger


class Agent(ABC):
    """Represents an abstract agent interacting with the world."""

    def __init__(self) -> None:
        Logger.info(f"This simulation is using a {self.__class__}")
