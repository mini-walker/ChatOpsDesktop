@echo off
REM -------------------------------
REM Remove old build/dist/spec
REM -------------------------------
rmdir /s /q EXE\build
rmdir /s /q EXE\dist
if exist GPTCombo.spec del GPTCombo.spec

REM -------------------------------
REM Generate exe with PyInstaller
REM Note: icon must be .ico, PNG does not work for exe icon
REM -------------------------------
pyinstaller --clean --windowed --noupx ^
--name "GPTCombo" ^
--workpath "EXE\build" ^
--distpath "EXE\dist" ^
--add-data "images;images" ^
--add-data "usr;usr" ^
--add-data "src;src" ^
--icon "images\AIchat_Combo_Logo.ico" ^
src\Main.py



echo.
echo =====================================================
echo  Build complete!
echo  Executable is in EXE\dist\yPlus_Calculator\
echo  Run by double-clicking yPlus_Calculator.exe
echo =====================================================
pause



