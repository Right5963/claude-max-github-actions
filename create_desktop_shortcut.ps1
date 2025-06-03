# デスクトップショートカット作成スクリプト
# Claude Code を1クリックで起動できるようにする

param(
    [switch]$Force
)

Write-Host "🔗 Claude Code デスクトップショートカット作成" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan

# パス設定
$desktopPath = [Environment]::GetFolderPath("Desktop")
$shortcutPath = Join-Path $desktopPath "Claude Code Quick Launch.lnk"
$targetPath = "C:\Claude Code\tool\claude_quick_launch.bat"
$iconPath = "C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"

# 既存ショートカットチェック
if ((Test-Path $shortcutPath) -and (-not $Force)) {
    $choice = Read-Host "既存のショートカットが見つかりました。上書きしますか？ (y/n)"
    if ($choice -ne 'y' -and $choice -ne 'Y') {
        Write-Host "❌ ショートカット作成をキャンセルしました" -ForegroundColor Yellow
        exit 0
    }
}

# ショートカット作成
try {
    $shell = New-Object -ComObject WScript.Shell
    $shortcut = $shell.CreateShortcut($shortcutPath)
    $shortcut.TargetPath = $targetPath
    $shortcut.WorkingDirectory = "C:\Claude Code\tool"
    $shortcut.Description = "Claude Code - AI開発アシスタント (ワンクリック起動)"
    $shortcut.IconLocation = "$iconPath,0"
    $shortcut.WindowStyle = 1  # 通常ウィンドウ
    $shortcut.Save()
    
    Write-Host "✅ ショートカット作成完了!" -ForegroundColor Green
    Write-Host "📁 場所: $shortcutPath" -ForegroundColor White
    
    # 追加のショートカット（PowerShell版）
    $psShortcutPath = Join-Path $desktopPath "Claude Code (Advanced).lnk"
    $psShortcut = $shell.CreateShortcut($psShortcutPath)
    $psShortcut.TargetPath = "powershell.exe"
    $psShortcut.Arguments = "-ExecutionPolicy Bypass -File `"C:\Claude Code\tool\claude_auto_start.ps1`""
    $psShortcut.WorkingDirectory = "C:\Claude Code\tool"
    $psShortcut.Description = "Claude Code - 高度な起動オプション付き"
    $psShortcut.IconLocation = "$iconPath,0"
    $psShortcut.Save()
    
    Write-Host "✅ 高度版ショートカットも作成完了!" -ForegroundColor Green
    Write-Host "📁 場所: $psShortcutPath" -ForegroundColor White
    
} catch {
    Write-Error "❌ ショートカット作成に失敗: $($_.Exception.Message)"
    exit 1
}

Write-Host ""
Write-Host "🎯 使用方法:" -ForegroundColor Yellow
Write-Host "  🖱️  デスクトップの 'Claude Code Quick Launch' をダブルクリック" -ForegroundColor White
Write-Host "  ⚡ 自動で Cursor → WSL → Claude Code の全手順が実行されます" -ForegroundColor White
Write-Host ""
Write-Host "🔧 高度な使用方法:" -ForegroundColor Yellow  
Write-Host "  🖱️  'Claude Code (Advanced)' で詳細オプション利用可能" -ForegroundColor White
Write-Host "  📝 パラメータ: -NewSession -SkipCursor -Quiet" -ForegroundColor White
Write-Host ""

# タスクバーピン留めの提案
$pinChoice = Read-Host "タスクバーにもピン留めしますか？ (y/n)"
if ($pinChoice -eq 'y' -or $pinChoice -eq 'Y') {
    try {
        # タスクバーピン留め（Windows 10/11対応）
        $pinVerbs = (New-Object -ComObject Shell.Application).NameSpace((Split-Path $shortcutPath)).ParseName((Split-Path $shortcutPath -Leaf)).Verbs()
        $pinVerb = $pinVerbs | Where-Object {$_.Name -like "*タスク*" -or $_.Name -like "*pin*"}
        if ($pinVerb) {
            $pinVerb.DoIt()
            Write-Host "📌 タスクバーにピン留めしました" -ForegroundColor Green
        } else {
            Write-Host "⚠️  タスクバーピン留めは手動で行ってください" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "⚠️  タスクバーピン留めは手動で行ってください" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "🎉 セットアップ完了！今後の起動は1クリックです！" -ForegroundColor Green