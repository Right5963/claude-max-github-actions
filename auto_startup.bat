@echo off
REM ===============================================
REM Obsidian-Cursor-Claude Code 自動起動システム
REM ===============================================

echo 🚀 Obsidian-Cursor-Claude Code システム自動起動中...
echo.

REM 作業ディレクトリに移動
cd /d "C:\Claude Code\tool"

REM Python環境確認
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python環境が見つかりません
    echo Python環境を設定してから再実行してください
    pause
    exit /b 1
)

echo ✅ Python環境確認完了

REM システム健全性チェック（高速版）
echo 📊 システム健全性チェック実行中...
python -c "from daily_workflow_optimizer import DailyWorkflowOptimizer; DailyWorkflowOptimizer().quick_health_check()"

REM 日常ワークフロー自動開始
echo.
echo 🌅 日常ワークフロー開始...
python -c "from daily_workflow_optimizer import DailyWorkflowOptimizer; DailyWorkflowOptimizer().start_daily_session()"

echo.
echo 🎉 自動起動完了！
echo.
echo 📝 次のアクション:
echo   1. Obsidian を開いて知識ベースを確認
echo   2. Cursor を開いてClaude連携開発を開始
echo   3. 必要に応じて詳細システム状況を確認: python system_health_simple.py
echo.

REM 自動終了を防ぐ（設定可能）
if "%1"=="--auto" (
    echo 🔄 自動モードで実行完了
    timeout /t 5 /nobreak >nul
) else (
    echo ⏸️ 任意のキーを押して終了...
    pause >nul
)
