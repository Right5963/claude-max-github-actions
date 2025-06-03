# Gドライブファイル操作関数

$VaultPath = "G:\マイドライブ\Obsidian Vault"

# ファイル読み込み
function Read-ObsidianNote {
    param([string]$NotePath)
    $FullPath = Join-Path $VaultPath $NotePath
    if (Test-Path $FullPath) {
        Get-Content $FullPath -Encoding UTF8
    } else {
        Write-Error "File not found: $FullPath"
    }
}

# ファイル書き込み
function Write-ObsidianNote {
    param(
        [string]$NotePath,
        [string]$Content
    )
    $FullPath = Join-Path $VaultPath $NotePath
    $Directory = Split-Path $FullPath -Parent
    
    if (!(Test-Path $Directory)) {
        New-Item -ItemType Directory -Path $Directory -Force
    }
    
    Set-Content -Path $FullPath -Value $Content -Encoding UTF8
    Write-Host "✅ Saved: $FullPath"
}

# ノート検索
function Search-ObsidianNotes {
    param([string]$Pattern)
    Get-ChildItem $VaultPath -Recurse -Filter "*.md" | 
        Select-String -Pattern $Pattern -Encoding UTF8 |
        Select-Object -Property Path, LineNumber, Line
}

# ファイル一覧
function Get-ObsidianNotes {
    param([string]$SubPath = "")
    $SearchPath = if ($SubPath) { Join-Path $VaultPath $SubPath } else { $VaultPath }
    Get-ChildItem $SearchPath -Filter "*.md" -Recurse | 
        Select-Object -Property Name, DirectoryName, LastWriteTime
}

# 使用例
Write-Host "=== Obsidian Vault File Operations ==="
Write-Host "VaultPath: $VaultPath"