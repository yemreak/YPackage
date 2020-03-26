@echo off

echo.
echo.
echo Python installation
echo -------------------
echo.

call pip install .

echo.
echo.
echo YThemeCreator - Base
echo -------------------
echo.


call ythemecreator.exe ../DarkCode-Theme/core/settings.json


echo.
echo.
echo YThemeCreator - Error
echo -------------------
echo.


call ythemecreator.exe ../DarkCode-Theme/core/darkcode.json


exit /B
