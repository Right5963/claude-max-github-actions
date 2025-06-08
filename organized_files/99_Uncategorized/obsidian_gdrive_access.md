# Obsidian Gドライブアクセス戦略

## 問題
- GドライブがWSLに直接マウントできない
- 管理者権限なしでジャンクション作成不可

## 解決策

### 1. Python同期スクリプト（推奨）
```bash
# Windows側で実行
python "C:\Claude Code\tool\sync_obsidian_from_gdrive.py"

# WSLからアクセス
cd "/mnt/c/Claude Code/tool/obsidian-vault-mirror"
grep -r "TAL" .
```

### 2. Windows側でのコマンド実行
```bash
# WSLから間接的にGドライブアクセス
cmd.exe /c "type \"G:\\マイドライブ\\Obsidian Vault\\file.md\""
cmd.exe /c "dir \"G:\\マイドライブ\\Obsidian Vault\" /b"
```

### 3. PowerShellを使用
```bash
# WSLからPowerShellコマンド実行
powershell.exe -Command "Get-Content 'G:\マイドライブ\Obsidian Vault\*.md' | Select-String 'TAL'"
```

### 4. 定期同期タスク
Windowsタスクスケジューラーで`sync_obsidian.bat`を定期実行

## 即座に使える方法

### TAL検索（Windows cmd経由）
```bash
cmd.exe /c "findstr /s /i \"TAL\" \"G:\\マイドライブ\\Obsidian Vault\\*.md\""
```

### ファイル一覧取得
```bash
cmd.exe /c "dir \"G:\\マイドライブ\\Obsidian Vault\" /s /b" | grep "\.md$"
```

### 特定ファイル読み込み
```bash
cmd.exe /c "type \"G:\\マイドライブ\\Obsidian Vault\\README.md\""
```