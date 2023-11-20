from inspect import getframeinfo, getmodulename, currentframe
from datetime import datetime
from loguru import logger as loguru_logger
from os import path as osp, getpid
from typing import Optional
from traceback import format_exception
from datetime import datetime
from qfluentwidgets import __version__ as pfwVer
from psutil import Process
from platform import (
    system as systemType,
    architecture as systemArchitecture,
    version as systemVersion,
    release as systemRelease,
    python_version as pythonVersion,
)


class _MCSL2Logger:
    def __init__(self):
        self.time = datetime.now().strftime("%Y-%m-%d_%H")
        self.logger = loguru_logger
        self.logger.add(
            self._getLogFile(),
            rotation="1 day",
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
        self.info(
            f"\nMCSL2 - 日志\n本次启动时刻：{str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}\n{genSysReport()}"
        )

    def _getLogFile(self) -> str:
        return osp.join("MCSL2/Logs", f"MCSL2_{self.time}.log")

    def _template(self, caller_info, msg) -> str:
        return f"{caller_info['module']}.{caller_info['function']}, at line {caller_info['line']} | {msg}"

    def info(self, msg: str):
        frame = getframeinfo(currentframe().f_back)
        caller_info = {
            "module": getmodulename(frame.filename),
            "filename": frame.filename,
            "line": frame.lineno,
            "function": frame.function,
        }
        self.logger.info(self._template(caller_info, msg))

    def warning(self, msg: str):
        frame = getframeinfo(currentframe().f_back)
        caller_info = {
            "module": getmodulename(frame.filename),
            "filename": frame.filename,
            "line": frame.lineno,
            "function": frame.function,
        }
        self.logger.warning(self._template(caller_info, msg))

    def success(self, msg: str):
        frame = getframeinfo(currentframe().f_back)
        caller_info = {
            "module": getmodulename(frame.filename),
            "filename": frame.filename,
            "line": frame.lineno,
            "function": frame.function,
        }
        self.logger.success(self._template(caller_info, msg))

    def error(self, exc: Optional[Exception] = None, msg: Optional[str] = ""):
        frame = getframeinfo(currentframe().f_back)
        caller_info = {
            "module": getmodulename(frame.filename),
            "filename": frame.filename,
            "line": frame.lineno,
            "function": frame.function,
        }
        excStr = ""
        if exc is not None:
            excStr = "".join(format_exception(type(exc), exc, exc.__traceback__))
        self.logger.error(self._template(caller_info, f"{msg}\n{excStr}"))

    def trace(self, msg: str):
        frame = getframeinfo(currentframe().f_back)
        caller_info = {
            "module": getmodulename(frame.filename),
            "filename": frame.filename,
            "line": frame.lineno,
            "function": frame.function,
        }
        self.logger.trace(self._template(caller_info, msg))

    def debug(self, msg: str):
        frame = getframeinfo(currentframe().f_back)
        caller_info = {
            "module": getmodulename(frame.filename),
            "filename": frame.filename,
            "line": frame.lineno,
            "function": frame.function,
        }
        self.logger.debug(self._template(caller_info, msg))

    def critical(self, exc: Optional[Exception] = None, msg: Optional[str] = ""):
        frame = getframeinfo(currentframe().f_back)
        caller_info = {
            "module": getmodulename(frame.filename),
            "filename": frame.filename,
            "line": frame.lineno,
            "function": frame.function,
        }
        excStr = "".join(format_exception(type(exc), exc, exc.__traceback__))
        self.logger.critical(self._template(caller_info, f"{msg}\n{excStr}"))


# Example usage
# logger = MCSL2Logger()
# logger.info("This is an info message.")
# logger.warning("This is a warning message.")
# logger.success("This is a success message.")
# logger.error(msg="This is an error message.", exc=TypeError("Test"))
# logger.trace("This is an trace message.")
# logger.debug("This is a debug message.")
# logger.critical("This is an critical message.")


def genSysReport() -> str:
    sysInfo = (
        f"{systemType()} {'11' if int(systemVersion().split('.')[-1]) >= 22000 else '10'} {systemVersion()}"
        if systemType() == "Windows" and systemRelease() == "10"
        else f"{systemType()} {systemRelease()}"
    )
    return (
        f"Python版本：{pythonVersion()}\n"
        f"控件库版本：{pfwVer}\n"
        f"操作系统：{sysInfo}\n"
        f"架构：{systemArchitecture()[0]}\n"
        f"内存占用：{str(round(Process(getpid()).memory_full_info().uss / 1024 / 1024, 2))}MB"
    )
