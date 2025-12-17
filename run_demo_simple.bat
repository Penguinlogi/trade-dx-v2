@echo off
echo =====================================
echo Phase 1 Demo Execution
echo =====================================
echo.

REM Get the directory where this batch file is located
set "SCRIPT_DIR=%~dp0"

echo Current Directory: %CD%
echo Script Directory: %SCRIPT_DIR%
echo.

REM Change to the script directory
cd /d "%SCRIPT_DIR%"
echo Changed to: %CD%
echo.

REM Check if the scripts\phase1 directory exists
if exist "scripts\phase1\demo_phase1.py" (
    echo Found: scripts\phase1\demo_phase1.py
    echo.
    echo Running demo...
    echo.
    cd scripts\phase1
    python demo_phase1.py
) else (
    echo ERROR: scripts\phase1\demo_phase1.py not found!
    echo.
    echo Please make sure you are in the correct directory:
    echo %SCRIPT_DIR%
    echo.
    echo Contents of current directory:
    dir /b
)

echo.
echo =====================================
pause













