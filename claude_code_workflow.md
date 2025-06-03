# Claude Code 効率的なワークフロー
作成日: 2025年6月1日

## Claude DesktopとClaude Codeの使い分け

### Claude Desktopの問題点
- チャット制限がすぐに来てしまう
- 長時間の開発作業には不向き

### Claude Code CLIの利点
- 長時間の作業が可能
- トークン効率が良い
- ターミナルベースで高速

## 推奨ワークフロー

### 1. 基本的な作業はClaude Code CLIで
```bash
# ファイル操作
cat file.txt           # ファイル読み込み
grep -r "pattern" .    # 検索
vim file.txt          # 編集

# Obsidianアクセス（直接）
cd "/mnt/c/Users/user/Documents/Obsidian Vault"
grep -r "TAL" .       # TAL関連情報を検索
```

### 2. 必要な時だけClaude Desktopを使用
- スクリーンショット取得が必要な時
- GUI操作が必要な時
- 短時間で終わるタスク

### 3. 代替ツールの活用

#### Obsidian操作
```bash
# MCP経由ではなく直接操作
OBSIDIAN_PATH="/mnt/c/Users/user/Documents/Obsidian Vault"

# 検索
grep -r "キーワード" "$OBSIDIAN_PATH"
rg "キーワード" "$OBSIDIAN_PATH"  # ripgrepの方が高速

# ノート作成
echo "# 新しいノート" > "$OBSIDIAN_PATH/新規ノート.md"

# ノート編集
vim "$OBSIDIAN_PATH/既存ノート.md"
```

#### ファイルシステム操作
```bash
# MCPを使わずに直接操作
find . -name "*.py" -type f
ls -la
cp source.txt dest.txt
```

## 効率化のヒント

### 1. エイリアス設定
```bash
# ~/.bashrcに追加
alias obs='cd "/mnt/c/Users/user/Documents/Obsidian Vault"'
alias obsg='grep -r "$1" "/mnt/c/Users/user/Documents/Obsidian Vault"'
```

### 2. スクリプト化
```bash
#!/bin/bash
# obsidian_search.sh
QUERY="$1"
VAULT="/mnt/c/Users/user/Documents/Obsidian Vault"
echo "=== Obsidian検索: $QUERY ==="
rg "$QUERY" "$VAULT" --type md
```

### 3. CLAUDE.mdの活用
- 重要な情報は常にCLAUDE.mdに記録
- セッション間での知識継承
- プロジェクト固有の設定を記載

## まとめ

Claude Code CLIは：
- ✅ 長時間作業に最適
- ✅ トークン効率が良い
- ✅ 標準ツールで十分な機能
- ❌ MCPツール直接利用は不可（代替手段あり）

Claude Desktopは：
- ✅ MCPツールが使える
- ✅ GUI操作が簡単
- ❌ チャット制限が厳しい
- ❌ 長時間作業に不向き

**結論**: Claude Code CLIをメインに使い、必要な時だけClaude Desktopを併用するのが最も効率的！