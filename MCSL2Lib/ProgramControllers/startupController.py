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
"""
Startup Controller
"""
import sys
from pathlib import Path
from platform import system


def _get_app_name() -> str:
    return "MCSL2"


def _build_launch_command() -> str:
    exe = Path(sys.executable).resolve()
    if getattr(sys, "frozen", False) or exe.suffix.lower() == ".exe":
        return f'"{str(exe)}"'
    script = Path(sys.argv[0]).resolve()
    if script.exists():
        return f'"{str(exe)}" "{str(script)}"'
    return f'"{str(exe)}"'


def is_start_on_startup_enabled() -> bool:
    if system().lower() != "windows":
        return False
    import winreg

    name = _get_app_name()
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_READ) as k:
            value, _typ = winreg.QueryValueEx(k, name)
            return bool((value or "").strip())
    except FileNotFoundError:
        return False
    except OSError:
        return False


def set_start_on_startup(enabled: bool) -> None:
    if system().lower() != "windows":
        raise RuntimeError("当前系统暂不支持开机自启动")
    import winreg

    name = _get_app_name()
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path) as k:
        if enabled:
            winreg.SetValueEx(k, name, 0, winreg.REG_SZ, _build_launch_command())
            return
        try:
            winreg.DeleteValue(k, name)
        except FileNotFoundError:
            return
