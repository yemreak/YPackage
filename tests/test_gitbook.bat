@echo off

echo.
echo.
echo Python installation
echo -------------------
echo.

call pip install .

echo.
echo.
echo Integrate - Base
echo -------------------
echo.


call ygitbookintegration ./YLib


echo.
echo.
echo Integrate - Recreate
echo -------------------
echo.


call ygitbookintegration ../IstanbulUniversity-CE -r


echo.
echo.
echo Integrate - Generate
echo -------------------
echo.


call ygitbookintegration ../IstanbulUniversity-CE -g


echo.
echo.
echo Integrate - More
echo -------------------
echo.


call ygitbookintegration ../IstanbulUniversity-CE ../YLib


echo.
echo.
echo Integrate - More - Debug
echo -------------------
echo.


call ygitbookintegration ../IstanbulUniversity-CE ../YLib -d


echo.
echo.
echo Integrate - More - Error
echo -------------------
echo.


call ygitbookintegration "../*"


echo.
echo.
echo Integrate - Dir
echo -------------------
echo.


call ygitbookintegration "../*"


echo.
echo.
echo Integrate - Push
echo -------------------
echo.


call ygitbookintegration ../YLib -usp


echo.
echo.
echo Integrate - Changelog
echo -------------------
echo.


call ygitbookintegration ../IstanbulUniversity-CE -c -ru https://github.com/YEmreAk/IstanbulUniversity-CE


echo.
echo.
echo Integrate - Changelog Push
echo -------------------
echo.


call ygitbookintegration ../IstanbulUniversity-CE -cp


echo.
echo.
echo Integrate - Complate
echo -------------------
echo.


call ygitbookintegration ../IstanbulUniversity-CE -rgcd -dl 2 -ru https://github.com/YEmreAk/IstanbulUniversity-CE -ic "💫 GitBook entegrasyonu yapıldı" "Merge branch """""master""""" of https://github.com/YEmreAk/IstanbulUniversity-CE" -cm "💫 GitBook entegrasyonu yapıldı"


echo.
echo.
echo Integrate - All
echo -------------------
echo.


call ygitbookintegration ../IstanbulUniversity-CE -rgc -dl 2 -ru https://github.com/YEmreAk/IstanbulUniversity-CE -ic "💫 GitBook entegrasyonu yapıldı" "Merge branch """""master""""" of https://github.com/YEmreAk/IstanbulUniversity-CE" -cm "💫 GitBook entegrasyonu yapıldı"


echo.
echo.
echo Integrate - All - Push
echo -------------------
echo.


call ygitbookintegration ../IstanbulUniversity-CE -rgcp -dl 2 -ru https://github.com/YEmreAk/IstanbulUniversity-CE -ic "💫 GitBook entegrasyonu yapıldı" "Merge branch """""master""""" of https://github.com/YEmreAk/IstanbulUniversity-CE" -cm "💫 GitBook entegrasyonu yapıldı"


exit /B
