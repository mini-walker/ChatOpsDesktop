@echo off
setlocal enabledelayedexpansion

echo.
echo ===== REMOVING SECRETS FROM GIT HISTORY =====
echo.
echo This script will remove usr/account.json from all commits
echo WARNING: This rewrites git history! Force push will be required.
echo.
pause

echo.
echo ===== Step 1: Ensure usr/account.json is in .gitignore =====
findstr /M "usr/account.json" .gitignore >nul
if errorlevel 1 (
    echo usr/account.json>>.gitignore
    echo [INFO] Added usr/account.json to .gitignore
) else (
    echo [INFO] usr/account.json already in .gitignore
)

echo.
echo ===== Step 2: Remove usr/account.json from all commits =====
echo Installing git-filter-repo if needed...
pip show git-filter-repo >nul 2>&1
if errorlevel 1 (
    echo Installing git-filter-repo...
    pip install git-filter-repo
)

echo.
echo Running git filter-repo to remove usr/account.json from history...
git filter-repo --path usr/account.json --invert-paths --force

if errorlevel 1 (
    echo [ERROR] git-filter-repo failed. Trying alternative method...
    echo.
    echo Falling back to git filter-branch...
    git filter-branch --tree-filter "git rm -f -r --cached usr/account.json; git clean -fd" --all --force
)

echo.
echo ===== Step 3: Verify the secret is removed =====
git log --all --source --full-history --name-only | findstr "account.json"
if errorlevel 1 (
    echo [SUCCESS] usr/account.json removed from all commits
) else (
    echo [WARNING] Some traces might remain - double check
)

echo.
echo ===== Step 4: Force push to GitHub =====
echo Performing force push to overwrite remote history...
git push origin main --force-with-lease

if errorlevel 1 (
    echo.
    echo [ERROR] Force push failed. Try:
    echo   git push origin main --force-with-lease
    echo   or
    echo   git push origin main --force
) else (
    echo [SUCCESS] Force push completed!
)

echo.
echo ===== Step 5: Notify GitHub to verify secret removal =====
echo.
echo Visit this link to verify secret removal:
echo https://github.com/mini-walker/ChatOpsDesktop/security/secret-scanning
echo.
echo If the secret still appears, it may take a few minutes for GitHub to update.
echo.

pause
