$PSScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $PSScriptRoot
& "$PSScriptRoot\.venv\Scripts\python.exe" -u orchestrate.py 2>&1 | Tee-Object -FilePath "$PSScriptRoot\pipeline.log" -Append
