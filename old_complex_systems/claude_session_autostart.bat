@echo off
REM Claude Code セッション自動監視起動
REM ==================================
REM Claude Code起動時に自動的に監視を開始

echo ========================================
echo   Claude Code セッション監視システム
echo ========================================
echo.

REM WSL内でセッション監視を開始
echo [1/3] セッション監視を開始しています...
wsl -e bash -c "cd '/mnt/c/Claude Code/tool' && ./session_monitor_launcher.sh start"
echo.

REM Claude Code起動
echo [2/3] Claude Codeを起動しています...
cd /d "C:\Claude Code\tool"
REM claude起動（既存のclaude_quick_launch.batを利用）
if exist "claude_quick_launch.bat" (
    call claude_quick_launch.bat
) else (
    REM claude_quick_launch.batがない場合は直接起動
    wsl -e claude
)

echo.
echo [3/3] 監視状態を確認しています...
wsl -e bash -c "cd '/mnt/c/Claude Code/tool' && ./session_monitor_launcher.sh status"

echo.
echo ========================================
echo セッション監視が有効になりました
echo 5分ごとに自動保存されます
echo ========================================
echo.
pause