import sys

from cx_Freeze import setup, Executable

build_exe_options = {
"include_msvcr": True   
}

base=None

if sys.platform=='win32':
    base="WIN32GUI"


setup(  name = "fly",
        version = "1.0",
        description = "pygame cxfreeze",
        options = {"build_exe": build_exe_options},
        executables = [Executable("play.py", base=base)]
)
