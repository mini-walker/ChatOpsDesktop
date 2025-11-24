@echo off
setlocal enabledelayedexpansion

rem ===== User Info: Only set on first-time use =====
rem git config --global user.name "mini-walker"
rem git config --global user.email "sjin@mun.ca"

echo.
echo ===== Step 0: Create .gitignore =====
echo # Auto-generated .gitignore > .gitignore
echo build/>>.gitignore
echo */build/>>.gitignore
echo */amrex_build/>>.gitignore
echo *.o>>.gitignore
echo *.a>>.gitignore
echo *.so>>.gitignore
echo *.exe>>.gitignore
echo *.dll>>.gitignore
echo *.log>>.gitignore
echo Git_Upload.bat>>.gitignore
rem echo *.obj>>.gitignore

echo [.gitignore created]


@echo off
setlocal enabledelayedexpansion

echo ===== Step 0: Create .gitignore =====
echo # Auto-generated .gitignore > .gitignore
echo build/>>.gitignore
echo */build/>>.gitignore
...
echo [.gitignore created]

echo ===== Step 1: Remove tracked "build" dirs =====
for /f "delims=" %%D in ('dir /ad /b /s build 2^>nul') do (
    echo Removing Git tracking from: %%D
    git rm -r --cached "%%D" >nul 2>nul
)

echo ===== Step 2: Init Git if not exists =====
IF NOT EXIST ".git" (
    git init
    git branch -M main
    echo [INFO] Git repository initialized
)

echo ===== Step 3: Set remote =====
git remote -v | findstr /C:"origin" >nul
IF ERRORLEVEL 1 (
    git remote add origin git@github.com:mini-walker/ChatOpsDesktop.git
    echo [INFO] Remote origin set
) ELSE (
    echo [INFO] Remote origin already exists
)

echo ===== Step 4: Stage all changes =====
git add -A

echo ===== Step 5: Auto commit if changes =====
for /f %%i in ('powershell -command "Get-Date -Format yyyy-MM-dd_HH:mm:ss"') do set timestamp=%%i
git diff-index --quiet HEAD || git commit -m "Auto commit at %timestamp%"

echo ===== Step 6: Pull remote =====
git pull origin main --allow-unrelated-histories --no-edit

echo ===== Step 7: Push to GitHub =====
git push origin main

echo [SUCCESS] Code has been pushed to GitHub.
pause
