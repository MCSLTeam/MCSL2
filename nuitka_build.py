# By shenjackyuanjie start from 20230818
# 求求 github action 大哥放我一马 能直接跑

import os
import sys
import subprocess

from typing import Tuple
from pathlib import Path

from lib_not_dr.nuitka.compile import CompilerHelper
from lib_not_dr.types.version import Version

def get_version() -> Tuple[Version, Version]:
    from MCSL2 import MAIN_VERSION, BUILD_VERSION
    return (MAIN_VERSION, BUILD_VERSION)


def gen_compiler() -> CompilerHelper:
    vers = get_version()
    compiler = CompilerHelper(
        src_file=Path("./MCSL2.py"),
        python_cmd=sys.executable,
        
        use_ccache=True,
        use_clang=True,
        use_lto=False,
        standalone=True,
        enable_console=True,
        
        show_progress=True,
        download_confirm=True,
        
        company_name="MCSL Team",
        product_name="MCSL 2",
        product_version=vers[0],
        file_version=vers[1],
        file_description="MC Server Launcher 2",
        
        copyright='Copyright ©MCSL Team. All right reserved.',
        
        icon_path=Path('./MCSL2.ico'),
        
        follow_import=['Adapters'],
        include_packages=['MCSL2Lib'],
        include_data_dir=[
            ('resource', 'resource'),
            ('MCSL2/Aria2', 'MCSL2/Aria2'),
        ],
        
        enable_plugin=['pyqt5'],
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
        compiler.output_path = Path("./build/github")
        sys.argv.remove("--github")

    if '--output' in sys.argv:
        compiler.output_path = Path(sys.argv[sys.argv.index('--output') + 1])
        sys.argv.remove('--output')
        sys.argv.remove(compiler.output_path.as_posix())

