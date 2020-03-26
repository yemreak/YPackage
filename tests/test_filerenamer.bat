@echo off

echo.
echo.
echo Python installation
echo -------------------
echo.

call pip install .

echo.
echo.
echo YFile - Base
echo -------------------
echo.


call yfilerenamer.exe . -p read -t mee


echo.
echo.
echo YFile - Group
echo -------------------
echo.


call yfilerenamer.exe . -p "(re)(ad)" -t "$2$1"


exit /B
