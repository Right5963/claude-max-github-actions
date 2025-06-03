@echo off
echo.
echo 🚀 ヤフオク完全自動化ツール
echo ========================
echo.
set /p keyword="キーワードを入力してEnter（例: アニメポスター）: "
echo.
cd /d "C:\Claude Code\tool"
python yahoo_auto.py %keyword%
pause