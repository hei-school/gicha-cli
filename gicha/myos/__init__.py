import platform
import os


def cd_then_exec(dir, windows_cmd, else_cmd):
    if "Windows" in platform.system():
        return os.system(f"cd /D {dir} && {windows_cmd}")
    else:
        return os.system(f"cd {dir} && {else_cmd}")
