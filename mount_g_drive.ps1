# GドライブWSLマウントスクリプト
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  GドライブをWSLにマウント" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# 管理者権限の確認
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator"))
{
    Write-Host "❌ 管理者権限が必要です" -ForegroundColor Red
    Write-Host "PowerShellを管理者として実行してください" -ForegroundColor Yellow
    Read-Host "Enterキーで終了"
    exit 1
}

# ジャンクション作成
$junctionPath = "C:\GDriveLink"
$targetPath = "G:\"

if (Test-Path $junctionPath) {
    Write-Host "🗑️ 既存のジャンクションを削除..." -ForegroundColor Yellow
    cmd /c rmdir "$junctionPath" 2>$null
}

Write-Host "📁 ジャンクションを作成..." -ForegroundColor Green
cmd /c mklink /J "$junctionPath" "$targetPath"

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ 成功！" -ForegroundColor Green
    Write-Host ""
    Write-Host "WSLからのアクセス方法:" -ForegroundColor Cyan
    Write-Host '  cd "/mnt/c/GDriveLink/マイドライブ/Obsidian Vault"' -ForegroundColor White
    Write-Host '  ls -la "/mnt/c/GDriveLink/マイドライブ/Obsidian Vault"' -ForegroundColor White
} else {
    Write-Host "❌ 失敗しました" -ForegroundColor Red
}

Write-Host ""
Read-Host "Enterキーで終了"