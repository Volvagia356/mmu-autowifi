rmdir /S /Q mmu-autowifi
python setup.py py2exe
cd dist
rename gui.exe mmu-autowifi.exe
del w9xpopen.exe
cd tcl/tcl8.5/
rmdir /S /Q encoding
rmdir /S /Q http1.0
rmdir /S /Q msgs
rmdir /S /Q opt0.4
rmdir /S /Q tzdata
del clock.tcl history.tcl package.tcl parray.tcl safe.tcl tm.tcl word.tcl
cd ../tk8.5/
rmdir /S /Q demos
rmdir /S /Q images
rmdir /S /Q msgs
cd ../../../
rename dist mmu-autowifi
pause