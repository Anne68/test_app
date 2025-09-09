@echo off
setlocal
cd /d "%~dp0"
".\.venv\Scripts\python.exe" -u orchestrate.py >> "pipeline.log" 2>&1
