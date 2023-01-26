from abc import ABC, abstractmethod


class BaseDump(ABC):

    @abstractmethod
    def write(self, path: str, body: str):
        pass
