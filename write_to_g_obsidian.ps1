$content = Get-Content 'C:\Claude Code\tool\MCP_Bridge_Complete_Guide.md' -Raw -Encoding UTF8
$path = 'G:\マイドライブ\Obsidian Vault\100_Cursor\MCP_Bridge_Complete_Guide_20250601.md'
$dir = Split-Path $path
if (!(Test-Path $dir)) {
    New-Item -Path $dir -ItemType Directory -Force | Out-Null
}
Set-Content -Path $path -Value $content -Encoding UTF8
Write-Host "ファイルを保存しました: $path"