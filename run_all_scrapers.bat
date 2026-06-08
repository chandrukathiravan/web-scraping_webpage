@echo off

cd /d "D:\chandru\web scraping_webpage"

REM ==========================================
REM Create Log Folder
REM ==========================================

if not exist Logs mkdir Logs

for /f %%i in ('powershell -command "Get-Date -Format yyyyMMdd"') do set TODAY=%%i

set LOGFILE=Logs\scraper_%TODAY%.log

echo ========================================== >> "%LOGFILE%"
echo STARTED : %date% %time% >> "%LOGFILE%"
echo ========================================== >> "%LOGFILE%"

echo Running DOMESTIC_DEPOSITS.py...
python DOMESTIC_DEPOSITS.py >> "%LOGFILE%" 2>&1

echo Running ROI_less_than_3cr.py...
python ROI_less_than_3cr.py >> "%LOGFILE%" 2>&1

echo Running Additional_Interest.py...
python Additional_Interest.py >> "%LOGFILE%" 2>&1

echo Running UCO_green_scheme.py...
python UCO_green_scheme.py >> "%LOGFILE%" 2>&1

echo Running Bulk_deposits.py...
python Bulk_deposits.py >> "%LOGFILE%" 2>&1

echo Running send_email.py...
python send_email.py >> "%LOGFILE%" 2>&1

echo ========================================== >> "%LOGFILE%"
echo COMPLETED : %date% %time% >> "%LOGFILE%"
echo ========================================== >> "%LOGFILE%"
