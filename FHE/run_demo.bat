@echo off
echo ========================================
echo FHE Officer Data Protection - Demo
echo ========================================
echo.

cd src

echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Running demo...
echo.
python officer_fhe.py

echo.
echo Demo completed!
pause

