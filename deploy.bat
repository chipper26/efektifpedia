@echo off
echo ===============================
echo 🚀 Deploy Hugo ke GitHub Pages
echo ===============================

cd /d %~dp0

echo.
echo [1/5] Build Hugo...
hugo -s .
IF %ERRORLEVEL% NEQ 0 (
  echo ❌ Hugo build gagal
  pause
  exit /b
)

echo.
echo [2/5] Salin hasil build ke root repo...
robocopy public . /E /NFL /NDL /NJH /NJS > nul

echo.
echo [3/5] Git add...
git add .

echo.
echo [4/5] Git commit...
git commit -m "deploy site"

echo.
echo [5/5] Git push...
git push

echo.
echo ✅ DEPLOY SELESAI
echo 🌐 https://chipper26.github.io/efektifpedia/
pause
