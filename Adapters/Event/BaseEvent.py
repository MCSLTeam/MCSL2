#     Copyright 2024, MCSL Team, mailto:services@mcsl.com.cn
#
#     Part of "MCSL2", a simple and multifunctional Minecraft server launcher.
#
#     Licensed under the GNU General Public License, Version 3.0, with our
#     additional agreements. (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#        https://github.com/MCSLTeam/MCSL2/raw/master/LICENSE
#
################################################################################
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

    """
            if func is not None and not callable(func):
            return
        tmpHandle
        self.handlers.append()
    """

    @abstractmethod
    def registerHandle(self, func, priority: int):
        pass

    @abstractmethod
    async def HandleEvent(self):
        pass
