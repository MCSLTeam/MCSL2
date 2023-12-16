from typing import List
from Adapters.Event.BaseEvent import BaseHandler, BaseEvent


class Handler(BaseHandler):
    def __init__(self):
        super().__init__()

    def setPriority(self, _priority: int):
        self.priority = _priority

    def register_func(self, func):
        if func is None:
            raise Exception("注册失败", None)
        self.handle_func = func

    @staticmethod
    def ToHandler(priority: int, handle_func):
        handler = Handler()
        handler.setPriority(priority)
        handler.register_func(handle_func)
        return handler


class Event(BaseEvent):
    def __init__(self):
        super().__init__()
        self.handlers: List[Handler] = []

    async def HandleEvent(self):
        for handler in self.handlers:
            try:
                await handler.handle_func()
            except Exception:
                raise Exception("事件处理错误")
