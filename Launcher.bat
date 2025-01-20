@echo off
setlocal
set PYTHONHOME=%~dp0\runtime\App\Python
set PYTHONPATH=%PYTHONHOME%\Lib;%PYTHONHOME%\DLLs
"%PYTHONHOME%\python.exe" "%~dp0\desktop-app\src\main.py"
endlocal
pause