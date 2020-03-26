@echo off

echo.
echo.
echo Python installation
echo -------------------
echo.

call pip install .

echo.
echo.
echo GSearch - Simple
echo -------------------
echo.


call ygooglesearch.exe site:yemreak.com


echo.
echo.
echo GSearch - Status Code
echo -------------------
echo.


call ygooglesearch.exe site:www.yemreak.com -sc 404


echo.
echo.
echo GSearch - Exclude
echo -------------------
echo.


call ygooglesearch.exe site:wiki.yemreak.com -ex knowed_url.txt


echo.
echo.
echo GSearch - Output
echo -------------------
echo.


call ygooglesearch.exe site:ai.yemreak.com site:windows.yemreak.com site:linux.yemreak.com site:ds.yemreak.com site:java.yemreak.com site:web.yemreak.com site:android.yemreak.com site:iuce.yemreak.com -sc 404 -o wrong_urls.txt


exit /B
