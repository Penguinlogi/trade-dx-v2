@echo off
REM Seed Data Execution Script

echo ========================================
echo Seed Data Execution Script
echo ========================================
echo.

cd /d %~dp0..

echo [1/2] Inserting seed data...
py -3 -m scripts.seed_data
if errorlevel 1 (
    echo.
    echo ERROR: Failed to insert seed data
    pause
    exit /b 1
)

echo.
echo [2/2] Inserting test data...
py -3 -m scripts.test_data
if errorlevel 1 (
    echo.
    echo ERROR: Failed to insert test data
    pause
    exit /b 1
)

echo.
echo ========================================
echo All data insertion completed
echo ========================================
pause
