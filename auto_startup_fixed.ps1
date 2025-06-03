# ===============================================
# Obsidian-Cursor-Claude Code 自動起動システム (修正版)
# ===============================================

param(
    [switch]$Auto,
    [switch]$Silent,
    [switch]$StartApps
)

Write-Host "🚀 Obsidian-Cursor-Claude Code システム自動起動中..." -ForegroundColor Green
Write-Host ""

# 作業ディレクトリに移動
Set-Location "C:\Claude Code\tool"

# Python環境確認
$pythonCheck = $false
try {
    $pythonResult = python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Python環境確認完了: $pythonResult" -ForegroundColor Green
        $pythonCheck = $true
    }
}
catch {
    Write-Host "❌ Python環境エラー" -ForegroundColor Red
}

if (-not $pythonCheck) {
    Write-Host "❌ Python環境が見つかりません" -ForegroundColor Red
    Write-Host "Python環境を設定してから再実行してください" -ForegroundColor Yellow
    if (-not $Auto) {
        Read-Host "Press Enter to exit"
    }
    exit 1
}

# システム健全性チェック（高速版）
if (-not $Silent) {
    Write-Host "📊 システム健全性チェック実行中..." -ForegroundColor Cyan
    python -c "from daily_workflow_optimizer import DailyWorkflowOptimizer; DailyWorkflowOptimizer().quick_health_check()"
}

# 日常ワークフロー自動開始
Write-Host ""
Write-Host "🌅 日常ワークフロー開始..." -ForegroundColor Cyan
python -c "from daily_workflow_optimizer import DailyWorkflowOptimizer; DailyWorkflowOptimizer().start_daily_session()"

# アプリケーション自動起動（オプション）
if ($StartApps) {
    Write-Host ""
    Write-Host "🎯 関連アプリケーション起動中..." -ForegroundColor Yellow

    # Obsidian起動試行
    $obsidianFound = $false
    try {
        $obsidianPath = Get-Command "Obsidian" -ErrorAction SilentlyContinue
        if ($obsidianPath) {
            Write-Host "📚 Obsidian起動中..." -ForegroundColor Blue
            Start-Process "Obsidian" -WindowStyle Minimized
            $obsidianFound = $true
        }
    }
    catch {
        Write-Host "⚠️ Obsidian起動エラー" -ForegroundColor Yellow
    }

    # Cursor起動試行
    $cursorFound = $false
    try {
        $cursorPath = Get-Command "cursor" -ErrorAction SilentlyContinue
        if ($cursorPath) {
            Write-Host "🖱️ Cursor起動中..." -ForegroundColor Blue
            Start-Process "cursor" "." -WindowStyle Minimized
            $cursorFound = $true
        }
    }
    catch {
        Write-Host "⚠️ Cursor起動エラー" -ForegroundColor Yellow
    }

    if (-not $obsidianFound -and -not $cursorFound) {
        Write-Host "ℹ️ Obsidian/Cursorが見つかりません。手動で起動してください" -ForegroundColor Cyan
    }
}

Write-Host ""
Write-Host "🎉 自動起動完了！" -ForegroundColor Green
Write-Host ""
Write-Host "📝 次のアクション:" -ForegroundColor Yellow
Write-Host "  1. Obsidian を開いて知識ベースを確認"
Write-Host "  2. Cursor を開いてClaude連携開発を開始"
Write-Host "  3. 必要に応じて詳細システム状況を確認: python system_health_simple.py"
Write-Host ""

# 終了処理
if ($Auto) {
    Write-Host "🔄 自動モードで実行完了" -ForegroundColor Cyan
    Start-Sleep -Seconds 3
} else {
    Write-Host "⏸️ 任意のキーを押して終了..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}
