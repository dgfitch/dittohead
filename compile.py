from distutils.core import setup
import py2exe

setup(
    windows = [
        {
            "script": "test.py",
            "icon_resources": [(1, "dittohead.ico")]
        }
    ],
)

# Run as python compile.py py2exe
# Locally, C:\dantemp\dev\PsychoPy2\python compile.py py2exe
