setlocal enabledelayedexpansion
echo off
title Matrix
color 02
mode 1000
cls
:prodolgit
set stroka=
for /l %%i in (0,1,200) do (
set /a vremenno=random%%2
)
set /a generate=random%
if %generate%==0 (color 0A) else (color 02)
echo %stroka%
goto prodolgit
