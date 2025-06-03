# Claude Code 自動起動スクリプト (PowerShell版)
# より高度な制御と設定が可能

param(
    [switch]$SkipCursor,      # Cursor起動をスキップ
    [switch]$NewSession,      # 新しいセッションを強制
    [switch]$Quiet,           # 静音モード
    [string]$WorkDir = "C:\Claude Code\tool"  # 作業ディレクトリ
)

# 関数定義
function Write-Status {
    param([string]$Message, [string]$Icon = "🎯")
    if (-not $Quiet) {
        Write-Host "$Icon $Message" -ForegroundColor Cyan
    }
}

function Test-ProcessRunning {
    param([string]$ProcessName)
    return (Get-Process -Name $ProcessName -ErrorAction SilentlyContinue) -ne $null
}

# メイン処理開始
Clear-Host
if (-not $Quiet) {
    Write-Host "========================================" -ForegroundColor Yellow
    Write-Host "    🚀 Claude Code 自動起動システム" -ForegroundColor Yellow  
    Write-Host "========================================" -ForegroundColor Yellow
    Write-Host ""
}

Write-Status "起動フロー分析中..."

# 1. Cursor起動チェック・制御
if (-not $SkipCursor) {
    if (Test-ProcessRunning "Cursor") {
        Write-Status "Cursor は既に起動中" "✅"
    } else {
        Write-Status "Cursor を起動中..." "📱"
        
        # Cursor実行ファイルの検索
        $cursorPaths = @(
            "$env:LOCALAPPDATA\Programs\cursor\Cursor.exe",
            "$env:APPDATA\Local\Programs\cursor\Cursor.exe",
            "C:\Program Files\Cursor\Cursor.exe"
        )
        
        $cursorFound = $false
        foreach ($path in $cursorPaths) {
            if (Test-Path $path) {
                Start-Process $path
                $cursorFound = $true
                break
            }
        }
        
        if (-not $cursorFound) {
            Write-Warning "⚠️ Cursor が見つかりません。手動で起動してください。"
        } else {
            Start-Sleep -Seconds 2
        }
    }
}

# 2. WSL利用可能性チェック
Write-Status "WSL 環境確認中..."
try {
    $wslCheck = wsl --status 2>$null
    Write-Status "WSL 利用可能" "✅"
} catch {
    Write-Error "❌ WSL が利用できません。Windows Subsystem for Linux を有効にしてください。"
    exit 1
}

# 3. 作業ディレクトリ確認
$wslWorkDir = $WorkDir -replace "C:", "/mnt/c" -replace "\\", "/"
Write-Status "作業ディレクトリ: $wslWorkDir"

# 4. セッション復元オプション
if ($NewSession) {
    Write-Status "新しいセッションを開始" "🆕"
    $sessionCmd = "echo '🆕 新しいセッションを開始します'"
} else {
    Write-Status "前回セッション復元中..." "🔄"
    $sessionCmd = "./session_restore.sh"
}

# 5. Claude Code 起動コマンド組み立て
$claudeCmd = @"
cd '$wslWorkDir' && 
echo '🎯 Claude Code 起動準備完了' && 
$sessionCmd && 
echo '' && 
echo '✅ Claude Code セッション開始!' && 
echo '💬 ご質問をどうぞ:' && 
claude
"@

Write-Status "Claude Code 起動中..." "🚀"
if (-not $Quiet) {
    Write-Host "💡 ヒント: 今後は" -ForegroundColor Green -NoNewline
    Write-Host " claude_quick_launch.bat " -ForegroundColor Yellow -NoNewline  
    Write-Host "をダブルクリックで即起動！" -ForegroundColor Green
    Write-Host ""
}

# 6. WSL経由でClaude Code実行
try {
    wsl -e bash -c $claudeCmd
} catch {
    Write-Error "❌ Claude Code の起動に失敗しました: $($_.Exception.Message)"
    exit 1
}

Write-Status "Claude Code セッション終了" "🎉"
if (-not $Quiet) {
    Write-Host ""
    Write-Host "次回起動方法:" -ForegroundColor Yellow
    Write-Host "  • デスクトップの claude_quick_launch.bat をダブルクリック" -ForegroundColor White
    Write-Host "  • または PowerShell で: .\claude_auto_start.ps1" -ForegroundColor White
    Write-Host ""
    Read-Host "Enterで終了"
}