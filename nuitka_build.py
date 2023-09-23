# By shenjackyuanjie start from 20230818
# 求求 github action 大哥放我一马 能直接跑
# 显灵了! 能跑!

"""
请各位修改之前一定要 @一下我 (shenjackyuanjie)
我也没找到啥时候把版本号丢到 variable 里面的
但是我谢谢你
要么发个 PR, 要么在群里 @一下 shenjack
反正一定跟我说一声
2023 09 17
"""

import sys
import time
import platform
import subprocess

from typing import Tuple
from pathlib import Path
from MCSL2Lib import VERSION, BUILD_VERSION  # 修改为直接放在 __init__ 里
from lib_not_dr.nuitka.compile import CompilerHelper
from lib_not_dr.types.version import Version


def get_version() -> Tuple[Version, Version]:
    # 尽量不要写死在构建脚本里
    return (Version(VERSION), Version(BUILD_VERSION))


def gen_compiler() -> CompilerHelper:
    vers = get_version()
    # for lib-not-dr 0.1.x
    # 0.2 估计要大改,反正先这样再说
    # 我 0.2 估计近一段时间反正出不来
    compiler = CompilerHelper(
        src_file=Path("./MCSL2.py"),
        python_cmd=sys.executable,
        use_ccache=True,
        use_clang=True,
        use_msvc=True,
        use_lto=False,
        standalone=True,
        enable_console=False,
        show_progress=True,
        download_confirm=True,
        remove_output=True,
        company_name="MCSL Team",
        product_name="MCSL 2",
        product_version=vers[0],
        file_version=vers[1],
        file_description="MC Server Launcher 2",
        copy_right="Copyright ©MCSL Team. All right reserved.",
        icon_path=Path("./MCSL2.ico"),
        no_follow_import=["numpy", "scipy"],
        follow_import=["Adapters"],
        include_packages=["MCSL2Lib"],
        include_data_dir=[
            ("MCSL2/Aria2", "MCSL2/Aria2"),
        ],
        enable_plugin=["pyqt5"],
    )
    return compiler


if __name__ == "__main__":
    compiler = gen_compiler()

    is_github = False
    if "--github" in sys.argv:
        is_github = True
        compiler.use_ccache = False
        compiler.show_memory = False
        compiler.show_progress = False
        compiler.enable_console = False
        compiler.output_path = Path("./build")
        sys.argv.remove("--github")

    if "--output" in sys.argv:
        compiler.output_path = Path(sys.argv[sys.argv.index("--output") + 1])
        sys.argv.remove("--output")
        sys.argv.remove(compiler.output_path.as_posix())


    if is_github:
        from pprint import pprint
        
        print(compiler.as_markdown(200))
        pprint(compiler.option())
    else:
        print(compiler.as_markdown())
        
        compiler.output_path = Path(f"./build/nuitka-{platform.system().lower()}")
    
    print(f"```bash\n{compiler.gen_subprocess_cmd()}\n```")

    # 确认是否需要编译
    # 如果包含 -y 参数 则直接编译
    if (("-y" or "-n") not in sys.argv) and (not is_github):
        while (do_compile := input("Do you want to compile this file? (y/n) ")) not in [
            "y",
            "n",
        ]:
            pass
    elif "-y" in sys.argv:
        do_compile = "y"
    elif is_github:
        do_compile = "y"
    else:
        do_compile = "n"

    if do_compile == "y":
        # 编译
        time.sleep(1)  # 等待 1s
        start_time = time.time_ns()
        subprocess.run(compiler.gen_subprocess_cmd())
        print("Compile Done!")
        print(
            f"Compile Time: {time.time_ns() - start_time} ns ({(time.time_ns() - start_time) / 1000_000_000} s)"
        )

    sys.exit(0)
