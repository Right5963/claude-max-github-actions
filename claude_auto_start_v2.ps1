# Claude Code 自動起動スクリプト (PowerShell版)
# Simple First原則の確認付き

Write-Host ""
Write-Host "🚨 Simple First 原則リマインダー" -ForegroundColor Yellow
Write-Host "====================================" -ForegroundColor Yellow
Write-Host "  73行のシンプルツール > 1,200行の複雑システム" -ForegroundColor Green
Write-Host "  技術的可能性に酔うな、実用性を追求せよ" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Yellow
Write-Host ""
Start-Sleep -Seconds 2

# WSLでClaude起動（Simple First確認付き）
wsl -e bash -c "cd '/mnt/c/Claude Code/tool' && /mnt/c/Claude\ Code/tool/claude_startup_check.sh && claude"