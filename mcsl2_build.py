import sys
from platform import system
from typing import List, Tuple
import time
import subprocess


class Arg:
    def __init__(self, value: str, command: str):
        self.cmd = f"{command}={value}"


class Args:
    def __init__(self, values: List[str], command: str):
        self.cmd = f"{command}={','.join(value for value in values)}"


class DescArg:
    def __init__(self, value: Tuple[str, str], command: str):
        self.cmd = f"{command}={value[0]}={value[1]}"


class Tag:
    def __init__(self, value: bool, command: str):
        if value:
            self.cmd = command
        else:
            self.cmd = ""


class MCSLCompiler:
    def __init__(self):
        # Python environment
        self.PYTHON_EXECUTABLE_PATH = sys.executable

        # Nuitka variables sets
        self.STANDALONE = Tag(True, "--standalone")
        self.ASSUME_YES_FOR_DOWNLOADS = Tag(True, "--assume-yes-for-download")
        self.MAIN = Arg("MCSL2.py", "--main")
        self.ICON = Arg(
            "MCSL2.ico",
            "--windows-icon-from-ico" if "windows" in system().lower() else "--linux-icon",
        )
        self.ENABLE_PLUGINS = Args(["pyqt5"], "--enable-plugin")

        # MCSL2 information
        import MCSL2Lib

        self.PRODUCT_VERSION = Arg(MCSL2Lib.MCSL2VERSION, "--product-version")
        self.BUILD_VERSION = Arg(MCSL2Lib.BUILD_VERSION, "--file-version")
        del MCSL2Lib
        self.COMPANY_NAME = Arg('"MCSL Team"', "--company-name")
        self.PRODUCT_NAME = Arg('"MCSL 2"', "--product-name")
        self.FILE_DESCRIPTION = Arg('"MCServerLauncher 2"', "--file-description")
        self.COPYRIGHT = Arg(
            '"Copyright © MCSL Team. All right reserved."',
            "--copyright",
        )

        # Packages and modules
        self.NO_FOLLOW_IMPORT = Args(
            ["numpy", "scipy", "PIL", "Pillow", "colorthief", "pyqt5-stubs"], "--nofollow-import-to"
        )
        self.FOLLOW_IMPORT = Args(["Adapters", "loguru", "requests"], "--follow-import-to")
        self.INCLUDE_PACKAGES = Args(["MCSL2Lib", "sqlite3"], "--include-package")

        # Data files
        self.INCLUDE_DATA_DIR = DescArg(("MCSL2/Aria2", "MCSL2/Aria2"), "--include-data-dir")

        # Backend C Compiler
        self.USE_MINGW = Tag(False, "--mingw64")
        self.USE_MSVC = Arg("latest", "--msvc")
        self.USE_CLANG = Tag(True, "--clang")
        self.LINK_TIME_OPTIMIZATION = Arg("no", "--lto")
        self.DISABLE_CCACHE = Tag(False, "--disable-ccache")

        # Output
        self.OUTPUT_DIR = Arg("build", "--output-dir")
        self.REMOVE_OUTPUT = Tag(True, "--remove-output")

        # Debug
        self.ENABLE_CONSOLE = Tag(True, "--enable-console")
        self.SHOW_PROGRESS = Tag(False, "--show-progress")

    def generateCommand(self):
        return str(
            self.PYTHON_EXECUTABLE_PATH
            + " -m nuitka "
            + " ".join(
                arg.cmd
                for arg in (
                    self.STANDALONE,
                    self.USE_MINGW,
                    self.USE_MSVC,
                    self.USE_CLANG,
                    self.LINK_TIME_OPTIMIZATION,
                    self.DISABLE_CCACHE,
                    self.SHOW_PROGRESS,
                    self.ASSUME_YES_FOR_DOWNLOADS,
                    self.ENABLE_CONSOLE,
                    self.ENABLE_PLUGINS,
                    self.ICON,
                    self.PRODUCT_VERSION,
                    self.BUILD_VERSION,
                    self.FILE_DESCRIPTION,
                    self.COMPANY_NAME,
                    self.PRODUCT_NAME,
                    self.COPYRIGHT,
                    self.FOLLOW_IMPORT,
                    self.NO_FOLLOW_IMPORT,
                    self.INCLUDE_PACKAGES,
                    self.INCLUDE_DATA_DIR,
                    self.OUTPUT_DIR,
                    self.REMOVE_OUTPUT,
                    self.MAIN,
                )
            ).replace("   ", " ")
        )


if __name__ == "__main__":
    compiler = MCSLCompiler()

    if "--clang" in sys.argv and "--mingw64" in sys.argv:
        raise SystemError("Can't use both --clang and --mingw64 at the same time")

    compiler.USE_CLANG = Tag(True, "--clang") if "--clang" in sys.argv else Tag(False, "--clang")
    compiler.USE_MSVC = Arg("latest", "--msvc") if "--msvc" in sys.argv else Tag(False, "--msvc")
    compiler.REMOVE_OUTPUT = (
        Tag(True, "--remove-output") if "--no-output" in sys.argv else Tag(False, "--remove-output")
    )
    compiler.SHOW_PROGRESS = (
        Tag(True, "--show-progress") if "--verbose" in sys.argv else Tag(False, "--show-progress")
    )

    if "--env-gh" in sys.argv:
        compiler.ENABLE_CONSOLE = Tag(False, "--enable-console")
        compiler.DISABLE_CCACHE = Tag(True, "--disable-ccache")
        compiler.USE_CLANG = Tag(True, "--clang")
        compiler.USE_MSVC = Arg("latest", "--msvc")

    if "--env-dev" in sys.argv:
        compiler.ENABLE_CONSOLE = Tag(True, "--enable-console")
        compiler.DISABLE_CCACHE = Tag(False, "--disable-ccache")

    cmd = compiler.generateCommand()
    print(cmd)
    print("=======================")

    # 确认是否需要编译
    # 如果包含 -y 参数 则直接编译
    if (("-y" or "-n") not in sys.argv) and ("--env-gh" not in sys.argv):
        while (do_compile := input("Do you want to compile this file? (y/n) ")) not in [
            "y",
            "n",
        ]:
            pass
    elif "-y" in sys.argv:
        do_compile = "y"
    elif "--env-gh" in sys.argv:
        do_compile = "y"
    else:
        do_compile = "n"

    if do_compile == "y":
        # 编译
        time.sleep(1)  # 等待 1s
        start_time = time.time_ns()
        subprocess.run(cmd)
        print("Compile Done!")
        print(f"===Compile Time: {(time.time_ns() - start_time) / 1000_000_000} s===")

    # if "--rp" in sys.argv:
    #     if "windows" in system().lower():
    #         print("Publishing Release Preview...")

    sys.exit(0)
