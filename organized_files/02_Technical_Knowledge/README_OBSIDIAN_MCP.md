# Obsidian MCP 完全ガイド

## 🚀 クイックスタート

1. **setup_obsidian_mcp.bat** をダブルクリック
2. Claude Desktopを再起動
3. 完了！

## 📚 使えるようになるMCPツール

### Obsidian専用ツール（推奨）
- `mcp_obsidian__search_notes` - キーワードでノート検索
- `mcp_obsidian__read_note` - 特定のノートを読む
- `mcp_obsidian__create_note` - 新しいノートを作成
- `mcp_obsidian__update_note` - 既存ノートを更新
- `mcp_obsidian__list_notes` - ノート一覧を取得
- `mcp_obsidian__get_tags` - 全タグを取得
- `mcp_obsidian__get_note_links` - ノートのリンクを取得

### ファイルシステムツール（補助）
- `mcp_filesystem-obsidian__list_directory` - ディレクトリ一覧
- `mcp_filesystem-obsidian__read_file` - ファイル読み込み
- `mcp_filesystem-obsidian__write_file` - ファイル書き込み

## 💡 使用例

### TALについて調べる
```
「mcp_obsidian__search_notesを使ってTALを検索して」
```

### 特定のノートを読む
```
「mcp_obsidian__read_noteでProjects/AI開発.mdを読んで」
```

### 新しいノートを作成
```
「mcp_obsidian__create_noteで今日の学習メモを作成」
```

## 🔧 トラブルシューティング

### MCPツールが表示されない場合
1. Claude Desktopを完全に終了（タスクトレイも確認）
2. `%APPDATA%\Claude\claude_desktop_config.json` を確認
3. Claude Desktopを管理者として実行

### Obsidian Vaultが見つからない場合
1. setup_obsidian_mcp.batを再実行
2. 手動でVaultのパスを入力

## 📝 メモ

- WSLやGドライブのマウント問題を完全に回避
- Obsidianの内部構造を理解したアクセスが可能
- タグ、リンク、メタデータにも対応