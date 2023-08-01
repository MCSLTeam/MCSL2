from abc import ABCMeta, abstractmethod

from typing import List


class BaseHandler(metaclass=ABCMeta):
    def __init__(self):
        self.priority: int = 0
        self.handle_func = None

    @abstractmethod
    def setPriority(self, _priority: int):
        pass

    @abstractmethod
    def register_func(self, func):
        pass

    @staticmethod
    @abstractmethod
    def ToHandler(priority: int, handle_func):
        pass


class BaseEvent(metaclass=ABCMeta):
    def __init__(self):
        self.eventType: str = None
        self.handlers: List[BaseHandler] = []

    '''
            if func is not None and not callable(func):
            return
        tmpHandle
        self.handlers.append()
    '''
    @abstractmethod
    def registerHandle(self,func,priority: int):
        pass

    @abstractmethod
    async def HandleEvent(self):
        pass
