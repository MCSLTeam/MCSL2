import ast
import subprocess
import sys
from pathlib import Path
from typing import Dict
from typing import List
from typing import Tuple


ROOT = Path(__file__).resolve().parent
MAIN_SCRIPT = ROOT / "MCSL2.py"
OUTPUT_DIR = ROOT / "build"
KEEPALIVE_INTERVAL_SECONDS = 60


def read_versions() -> Tuple[str, str]:
    init_path = ROOT / "MCSL2Lib" / "__init__.py"
    values: Dict[str, str] = {}
    for node in ast.parse(init_path.read_text(encoding="utf-8")).body:
        if not isinstance(node, ast.Assign) or len(node.targets) != 1:
            continue
        target = node.targets[0]
        if isinstance(target, ast.Name) and target.id in {"VERSION", "BUILD_VERSION"}:
            value = ast.literal_eval(node.value)
            if isinstance(value, str):
                values[target.id] = value
    return values.get("VERSION", "2.0"), values.get("BUILD_VERSION", "0.3")


def build_args(extra_args: List[str]) -> List[str]:
    version, build_version = read_versions()
    disable_console = "--disable-console" in extra_args
    extra_args = [arg for arg in extra_args if arg != "--disable-console"]
    args = [
        sys.executable,
        "-m",
        "nuitka",
        "--clang",
        "--lto=yes",
        f"--product-version={version}",
        f"--file-version={build_version}",
        "--product-name=MCSL 2",
        "--company-name=MCSLTeam",
        "--file-description=MCServerLauncher 2",
        "--copyright=Copyright (C) MCSLTeam. All rights reserved.",
        "--include-package=MCSL2Lib",
        "--include-package=sqlite3",
        "--follow-import-to=Adapters",
        "--follow-import-to=loguru",
        "--follow-import-to=requests",
        "--follow-import-to=croniter",
        "--follow-import-to=openai",
        "--follow-import-to=pytz",
        "--follow-import-to=pypdl",
        "--nofollow-import-to=numpy",
        "--nofollow-import-to=scipy",
        "--nofollow-import-to=PIL",
        "--nofollow-import-to=colorthief",
        "--nofollow-import-to=sqlite3.test",
        "--enable-plugins=pyqt5",
        "--assume-yes-for-downloads",
        f"--output-dir={OUTPUT_DIR}",
    ]
    if sys.platform == "win32":
        args.append("--standalone")
        args.append("--msvc=latest")
        args.append("--windows-icon-from-ico=MCSL2.ico")
        has_console_mode = any(arg.startswith("--windows-console-mode=") for arg in extra_args)
        if disable_console and not has_console_mode:
            args.append("--windows-console-mode=disable")
    elif sys.platform.startswith("linux"):
        args.append("--standalone")
        args.append("--linux-icon=MCSL2.ico")
    elif sys.platform == "darwin":
        args.append("--mode=app")
        args.append("--macos-app-mode=gui")
        args.append("--macos-app-icon=MCSL2.icns")
        args.append(f"--macos-app-version={version}")
        args.append("--macos-prohibit-multiple-instances")
        args.append("--macos-signed-app-name=cn.mcslteam.mcsl2")

    args.extend(extra_args)
    args.append(str(MAIN_SCRIPT))
    return args


def main() -> int:
    command = build_args(sys.argv[1:])
    print(" ".join(command), flush=True)

    process = subprocess.Popen(command)
    try:
        while True:
            try:
                return process.wait(timeout=KEEPALIVE_INTERVAL_SECONDS)
            except subprocess.TimeoutExpired:
                print("Still running Nuitka build...", flush=True)
    except KeyboardInterrupt:
        process.terminate()
        raise


if __name__ == "__main__":
    raise SystemExit(main())
