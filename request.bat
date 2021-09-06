@echo off
cls
set /p min_percentage=Minimum profit percentage:
set /p members=Include Members items? (y/n):
set /p min_vol=Minimum volume[enter to skip]:
set /p min_margin=Minimum margin[enter to skip]:
if "%members%" == "y" set members=true
if not "%members%" == "true" set members=false
if "%min_vol%" == "" set min_vol=0
if "%min_margin%" == "" set min_vol=0
:a
cls
python flipper.py %min_percentage% %members% %min_vol% %min_margin%
pause
goto a