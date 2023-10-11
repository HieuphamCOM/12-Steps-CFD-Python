@echo off

set "userProfile=C:\Users\hieu.pham\Documents\gsi-formwork"

pushd "C:\ProgramData\Nemetschek\Allplan_2024_Verification\2024\Etc\Library\PythonParts"
mklink /j Formwork "C:\Users\hieu.pham\Documents\gsi-formwork\Library\PythonParts\Formwork"
popd

pushd "C:\ProgramData\Nemetschek\Allplan_2024_Verification\2024\Etc\PythonPartsScripts"
mklink /j Formwork "C:\Users\hieu.pham\Documents\gsi-formwork\PythonPartsContent\Formwork"
popd

rem Add another folder link here
pushd "C:\ProgramData\Nemetschek\Allplan_2024_Verification\2024\Etc\Library\"
mklink /j Construction "C:\Users\hieu.pham\Documents\gsi-formwork\Library\Construction"
popd

rem Add another folder link here
pushd "C:\TestAutomation\TestSuites\Allplan\DATA\Startdaten\UnitTests\Symbols\"
mklink /j Formwork "C:\Users\hieu.pham\Documents\gsi-formwork\Symbols\Formwork"
popd

ECHO Use just link file to Allplan 2024 Verification
PAUSE
