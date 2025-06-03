@echo off
REM Python実行ラッパー - Windows環境の問題回避
setlocal

REM Python Launcherを優先
py -3 %*
if %ERRORLEVEL% neq 0 (
    REM フォールバックでpythonコマンドを試行
    python %*
)
