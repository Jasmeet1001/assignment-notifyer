@echo off

set path_exe=%~dp0Assignment-Notifier.exe
set path_cred=%~dp0GetCredentials.exe

reg add HKLM\Software\Microsoft\Windows\CurrentVersion\Run /v Notifier /d %path_exe%

start "ERP Assignment Notifier" %path_cred%
