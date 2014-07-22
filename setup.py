from distutils.core import setup
import py2exe


setup(windows=['gui.py'],
    options={"py2exe": {
    'bundle_files': 3,
    'compressed': True}},
    zipfile = None,
    dlls_in_exedir = ["tcl85.dll", "tk85.dll"], data_files=["cabundle"])