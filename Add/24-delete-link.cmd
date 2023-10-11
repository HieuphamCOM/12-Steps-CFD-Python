@echo off

set "targetFolder1=C:\ProgramData\Nemetschek\Allplan_2024_Verification\2024\Etc\Library\PythonParts\Formwork"
set "targetFolder2=C:\ProgramData\Nemetschek\Allplan_2024_Verification\2024\Etc\Library\Construction"
set "targetFolder3=C:\ProgramData\Nemetschek\Allplan_2024_Verification\2024\Etc\PythonPartsScripts\Formwork"
set "targetFolder4=C:\TestAutomation\TestSuites\Allplan\DATA\Startdaten\UnitTests\Symbols\Formwork"

rem Check and delete Folder 1 if found
if exist "%targetFolder1%" (
    echo Finding...Folder "Etc\Library\PythonParts\Formwork" found. Deleting Folder ...
    rd /s /q "%targetFolder1%"
    echo Deleted successfully.
) else (
    echo Folder "Etc\Library\PythonParts\Formwork" not found. Nothing to do.
)

rem Check and delete Folder 2 if found
if exist "%targetFolder2%" (
    echo Finding...Folder "Etc\Library\Construction" found. Deleting Folder ...
    rd /s /q "%targetFolder2%"
    echo Deleted successfully.
) else (
    echo Folder "Etc\Library\Construction" not found. Nothing to do.
)

rem Check and delete Folder 3 if found
if exist "%targetFolder3%" (
    echo Finding...Folder "Etc\PythonPartsScripts\Formwork" found. Deleting Folder ...
    rd /s /q "%targetFolder3%"
    echo Deleted successfully.
) else (
    echo Folder "Etc\PythonPartsScripts\Formwork" not found. Nothing to do.
)

rem Check and delete Folder 4 if found
if exist "%targetFolder4%" (
    echo Finding...Folder "UnitTests\Symbols\Formwork" found. Deleting Folder ...
    rd /s /q "%targetFolder4%"
    echo Deleted successfully.
) else (
    echo Folder "UnitTests\Symbols\Formwork" not found. Nothing to do.
)


ECHO Use just link file to Allplan 2024 Verification
pause
