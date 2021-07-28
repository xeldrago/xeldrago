@echo off
title Batch Calculator by xeldrago
color 1f
:top
echo --------------------------------------------------------------
echo Welcome to Batch Calculator by xeldrago
echo --------------------------------------------------------------
echo basically you just use the keyboard signs to write your equation for answer ehehehe
echo.
set /p sum=
set /a ans=%sum%
echo.
echo = %ans%
echo --------------------------------------------------------------
pause
cls
echo Previous Answer: %ans%
goto top
pause
exit