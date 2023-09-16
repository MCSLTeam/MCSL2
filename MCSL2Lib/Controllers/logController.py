from inspect import getframeinfo, getmodulename, getsourcefile, currentframe
from datetime import datetime
from loguru import logger as loguru_logger
from loguru._logger import Logger
from loguru._logger import Core as _Core
from os import path as osp
from typing import Optional
from traceback import format_exception
# from colorama import 
# from MCSL2Lib.singleton import Singleton

# @Singleton
class MCSL2Logger:
    def __init__(self):
        self.logger = loguru_logger
        # self.logger.remove()
        self.logger.add(
            self._getLogFile(),
            rotation="30 s",
            retention="14 days",
            level="DEBUG",
            enqueue=True,
            backtrace=True,
            diagnose=True,
            compression="zip",
            catch=True,
            encoding="utf-8",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        )

    def _getLogFile(self) -> str:
        return osp.join(
            "MCSL2/Logs", f"{datetime.now().strftime('%Y-%m-%d_%H-%M')}.log"
        )

    def _template(self, caller_info, msg) -> str:
        return f"{caller_info['module']}.{caller_info['function']}, at line {caller_info['line']} | {msg}"

    def getCallerInfo(self) -> dict:
        frame = getframeinfo(currentframe().f_back)
        moduleName = getmodulename(frame.filename)
        return {
            "module": moduleName,
            "filename": frame.filename,
            "line": frame.lineno,
            "function": frame.function,
        }

    def info(self, msg: str):
        caller_info = self.getCallerInfo()
        self.logger.info(self._template(caller_info, msg))

    def warning(self, msg: str):
        caller_info = self.getCallerInfo()
        self.logger.warning(self._template(caller_info, msg))

    def success(self, msg: str):
        caller_info = self.getCallerInfo()
        self.logger.success(self._template(caller_info, msg))

    def error(self, exc: Optional[Exception] = None, msg: Optional[str] = ""):
        caller_info = self.getCallerInfo()
        excStr = "".join(format_exception(type(exc), exc, exc.__traceback__))
        self.logger.error(self._template(caller_info, f"{msg}\n{excStr}"))

    def trace(self, msg: str):
        caller_info = self.getCallerInfo()
        self.logger.trace(self._template(caller_info, msg))

    def debug(self, msg: str):
        caller_info = self.getCallerInfo()
        self.logger.debug(self._template(caller_info, msg))

    def critical(self, msg: str):
        caller_info = self.getCallerInfo()
        self.logger.critical(self._template(caller_info, msg))


# Example usage
logger = MCSL2Logger()
logger.info("This is an info message.")
logger.warning("This is a warning message.")
logger.success("This is a success message.")
logger.error(msg="This is an error message.", exc=TypeError("Test"))
logger.trace("This is an trace message.")
logger.debug("This is a debug message.")
logger.critical("This is an critical message.")