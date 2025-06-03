@echo off
chcp 65001 >nul
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                🚀 ヤフオクAI自動化システム                    ║
echo ║                     ボタン一発完全自動化                      ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

REM 引数チェック
if "%1"=="" (
    echo 使用方法: %~nx0 "キーワード" [生成枚数]
    echo 例: %~nx0 "アニメ 美少女" 20
    echo.
    set /p keyword=キーワードを入力してください: 
    set /p count=生成枚数を入力してください（デフォルト: 10）: 
    if "!count!"=="" set count=10
) else (
    set keyword=%1
    set count=%2
    if "!count!"=="" set count=10
)

echo.
echo 🎯 設定確認:
echo    キーワード: %keyword%
echo    生成予定枚数: %count%枚
echo.
pause

echo ⚡ 自動化開始...
echo.

REM WSLでPythonスクリプト実行
wsl -e bash -c "cd '/mnt/c/Claude Code/tool' && python3 one_click_automation.py '%keyword%' %count%"

echo.
echo ✅ 処理完了！生成された画像は results フォルダを確認してください。
echo.
pause