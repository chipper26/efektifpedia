@echo off
echo Build Hugo...
hugo || goto :error

echo Deploy hasil build ke root repo...
robocopy public . /E /XD .git

echo Done.
pause
exit /b 0

:error
echo Hugo build gagal
pause
exit /b 1