from cx_Freeze import setup, Executable
import os
os.environ['TCL_LIBRARY'] = "C:\\Python\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "C:\\Python\\tcl\\tk8.6"

base = None
executables = [Executable("main.py", base=base)]

packages = ["idna", "time", "math", "pygame", "sys", "random"]
buildOptions = dict(include_files = []) #folder,relative path. Use tuple like in the single file to set a absolute path.


options = {
    'build_exe': {
        'packages':packages,
    },
}

setup(
         name = "particle box",
         version = "1.0",
         description = "fun sandbox",
         author = "Tommy",
         options = dict(build_exe = buildOptions),
         executables = executables)

