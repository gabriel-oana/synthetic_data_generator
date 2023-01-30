from abc import ABC, abstractmethod


class BaseConverter(ABC):

    @abstractmethod
    def create(self, *args, **kwargs):
        raise NotImplementedError
