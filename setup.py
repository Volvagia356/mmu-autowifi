from distutils.core import setup
import py2exe

# Replace linux import with windows
orig = open("mmu_autowifi.py",'rb').read()
edited = orig.replace("from linux import", "from windows import")
open("mmu_autowifi.py",'wb').write(edited)

setup(windows=[{
		'script': 'gui.py',
		'icon_resources': [(1, "logo.ico")]
	}],
    options={"py2exe": {
    'bundle_files': 3,
    'compressed': True}},
    zipfile = None,
    data_files=["cabundle"])

open("mmu_autowifi.py",'wb').write(orig)