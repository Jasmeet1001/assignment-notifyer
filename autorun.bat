@echo off
set path_exe=%~dp0ERP_Notifier.exe
reg add HKLM\Software\Microsoft\Windows\CurrentVersion\Run /v Notifier /d %path_exe%

break>"C:\Users\Master\Documents\ERPNotifier\usr_word.txt"
