@echo off
echo ========================================
echo FHE Officer Data Protection - Tests
echo ========================================
echo.

cd src

echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Running tests...
echo.
python test_fhe.py

echo.
echo Tests completed!
pause

