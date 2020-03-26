@echo off

echo.
echo.
echo Python installation
echo -------------------
echo.

call pip install .

echo.
echo.
echo GDrive - Base
echo -------------------
echo.


call ygoogledrive.exe "https://drive.google.com/open?id=1H6W_NiMSKJqAbeQfJC0pABiCq6j-klEb"


echo.
echo.
echo GDrive - Reverse
echo -------------------
echo.


call ygoogledrive.exe "https://drive.google.com/uc?id=1H6W_NiMSKJqAbeQfJC0pABiCq6j-klEb" -r


echo.
echo.
echo GDrive - ID
echo -------------------
echo.


call ygoogledrive.exe "https://drive.google.com/uc?id=1H6W_NiMSKJqAbeQfJC0pABiCq6j-klEb"


exit /B
