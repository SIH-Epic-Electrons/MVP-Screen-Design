@echo off
echo ========================================
echo FHE Officer Data Protection
echo Complete Test Suite
echo ========================================
echo.

cd src

echo Step 1: Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo Step 2: Running demo...
echo.
python officer_fhe.py
if errorlevel 1 (
    echo ERROR: Demo failed
    pause
    exit /b 1
)

echo.
echo Step 3: Running tests...
echo.
python test_fhe.py
if errorlevel 1 (
    echo ERROR: Tests failed
    pause
    exit /b 1
)

echo.
echo ========================================
echo All operations completed successfully!
echo ========================================
pause

