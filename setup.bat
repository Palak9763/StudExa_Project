@echo off
echo ======================================
echo   StudExa - Student Progress Monitor
echo   Setup Script (Windows)
echo ======================================
echo.

echo [1/4] Installing dependencies...
pip install django pillow
echo.

echo [2/4] Setting up database...
python manage.py makemigrations
python manage.py migrate
echo.

echo [3/4] Seeding initial data...
python manage.py seed_data
echo.

echo [4/4] Creating media folders...
if not exist "media\proofs" mkdir media\proofs
if not exist "media\profiles" mkdir media\profiles
echo.

echo ======================================
echo  Setup complete!
echo.
echo  Run:   python manage.py runserver
echo  Open:  http://127.0.0.1:8000
echo.
echo  Login credentials:
echo    Admin:   admin@spms.com   / admin123
echo    Faculty: faculty@spms.com / faculty123
echo    Student: student@spms.com / student123
echo ======================================
pause
