from distutils.core import setup
import py2exe

setup(
    options = {
        "py2exe": {
            "dll_excludes": ["MSVCP90.dll"],
            'optimize': 2,
            'bundle_files': 1,
            'dist_dir': 'win_dist',
        },
        "build": {
            'build_base': 'win_build',
        }
    },
    windows = [
        {
            "script": "dittohead.py",
            "icon_resources": [(1, "dittohead.ico")],
        },
    ],
    zipfile = None,
)

# Run as python win_compile.py py2exe
# TODO: Figure out how to copy *.yaml and *.ico to dist directory
