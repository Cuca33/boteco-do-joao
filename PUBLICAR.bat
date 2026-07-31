@echo off
chcp 65001 >nul
title Publicar cardapio - Boteco do Joao
set PY=C:\Users\User\AppData\Local\Programs\Python\Python313\python.exe
if not exist "%PY%" set PY=python
"%PY%" "%~dp0publicar.py" %*
echo.
pause
