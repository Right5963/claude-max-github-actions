@echo off
REM Claude Code クイック起動 - ワンクリックで完全自動化
REM 現在の手順: Cursor起動 → PowerShell → wsl → claude
REM 新しい手順: このbatファイルをダブルクリックするだけ

echo.
echo ========================================
echo    🚀 Claude Code クイック起動
echo ========================================
echo.

REM 1. Cursorが起動中かチェック
tasklist /FI "IMAGENAME eq Cursor.exe" 2>NUL | find /I /N "Cursor.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo ✅ Cursor は既に起動中
) else (
    echo 📱 Cursor を起動中...
    start "" "C:\Users\%USERNAME%\AppData\Local\Programs\cursor\Cursor.exe"
    timeout /t 3 >nul
)

REM 2. 作業ディレクトリに移動してClaude Code起動
echo 🎯 Claude Code を起動中...
echo    💡 セッション復元機能が自動実行されます
echo.

REM 3. 自動保存機能を起動（新しい監視システムを使用）
echo 📝 セッション自動監視を開始...
wsl -e bash -c "cd '/mnt/c/Claude Code/tool' && ./session_monitor_launcher.sh start > /dev/null 2>&1"
timeout /t 2 >nul

REM 4. Simple First原則の確認
echo.
echo 🚨 Simple First 原則リマインダー
echo ====================================
echo    73行のシンプルツール > 1,200行の複雑システム
echo    技術的可能性に酔うな、実用性を追求せよ
echo ====================================
echo.
timeout /t 3 >nul

REM 5. WSL経由でClaude Code起動 + セッション復元 + 重要リマインダー
wsl -e bash -c "cd '/mnt/c/Claude Code/tool' && echo '🔄 前回セッションを確認中...' && ./session_restore.sh && echo '' && ./claude_startup_reminders.sh && echo '✅ Claude Code 準備完了!' && echo '💬 質問や作業内容を入力してください:' && claude"

echo.
echo 🎉 Claude Code セッション終了
pause