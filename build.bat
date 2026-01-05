@echo off
echo Building AO Fishing Macro...
echo.

REM Check if PyInstaller is installed
python -c "import PyInstaller" 2>NUL
if errorlevel 1 (
    echo PyInstaller not found. Installing...
    pip install pyinstaller
    echo.
)

REM Build the executable using the spec file
echo Building executable...
pyinstaller build_exe.spec --clean

echo.
echo Build complete!
echo The executable is located in: dist\AO-Fishing-Macro.exe
echo.
pause
