@echo off
set "BASE=C:\Users\PC\.skillhub"
set "CLI=%BASE%\skills_store_cli.py"
set "PYTHON=C:\Users\PC\AppData\Local\Programs\Python\Python312\python.exe"
if not exist "%CLI%" (
  echo Error: CLI not found at %CLI%
  exit /b 1
)
if not exist "%PYTHON%" (
  echo Error: Python not found at %PYTHON%
  exit /b 1
)
"%PYTHON%" "%CLI%" %*
