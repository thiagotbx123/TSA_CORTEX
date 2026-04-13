@echo off
REM KPI Dashboard: rebuild + serve + system tray icon
REM Usage: double-click shortcut or run from terminal
cd /d "C:\Users\adm_r\Tools\TSA_CORTEX\scripts\kpi"
start "" "C:\Python314\pythonw.exe" "C:\Users\adm_r\Tools\TSA_CORTEX\scripts\kpi\kpi_tray.py"
