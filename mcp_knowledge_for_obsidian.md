# Claude Code MCP設定ガイド

## 設定完了日時
2025年1月6日 3:35 JST

## 設定済みMCPサーバー一覧

### 1. Obsidian MCP (`obsidian`)
```bash
claude mcp add obsidian -- npx -y @cedricchee/mcp-obsidian "G:\\マイドライブ\\Obsidian Vault"
```
- **用途**: Obsidianノートの検索、読み込み、作成、更新
- **パス**: G:\マイドライブ\Obsidian Vault

### 2. Filesystem MCP (複数設定)

#### Tool Directory (`filesystem`)
```bash
claude mcp add filesystem -- npx -y @modelcontextprotocol/server-filesystem "/mnt/c/Claude Code/tool"
```

#### G Drive Obsidian (`filesystem-gdrive`)
```bash
claude mcp add filesystem-gdrive -- npx -y @modelcontextprotocol/server-filesystem "G:\\マイドライブ\\Obsidian Vault"
```

#### MCP Directory (`filesystem-mcp`)
```bash
claude mcp add filesystem-mcp -- npx -y @modelcontextprotocol/server-filesystem "/mnt/c/Claude Code/MCP"
```

### 3. Desktop Commander (`desktop-commander`)
```bash
claude mcp add desktop-commander -- npx -y @wonderwhy-er/desktop-commander@latest
```
- **用途**: スクリーンショット取得、ウィンドウ操作、システム情報取得

### 4. Memory MCP (`memory`)
```bash
claude mcp add memory -- npx -y @modelcontextprotocol/server-memory
```
- **用途**: セッション間での情報永続化、キーバリューストア

### 5. Playwright MCP (`playwright`)
```bash
claude mcp add playwright -- npx -y @playwright/mcp@latest
```
- **用途**: ブラウザ自動化、Webページ操作、スクレイピング

### 6. SQLite MCP (`sqlite`)
```bash
claude mcp add sqlite -- uvx mcp-server-sqlite --db-path "/mnt/c/Claude Code/MCP/data/knowledge.db"
```
- **用途**: SQLiteデータベース操作、知識管理

### 7. Note API (`note-api`)
```bash
claude mcp add note-api -- node "/mnt/c/Claude Code/MCP/note-mcp-server/build/note-mcp-server-refactored.js"
```
- **用途**: Note.com APIアクセス

## MCP基本コマンド

```bash
# MCPサーバー一覧表示
claude mcp list

# MCPサーバー追加
claude mcp add <name> -- <command> [args...]

# MCPサーバー削除
claude mcp remove <name>

# MCPサーバー詳細表示
claude mcp get <name>
```

## スコープオプション

- `--scope local` (デフォルト): 現在のプロジェクトのみ
- `--scope project`: チームで共有（.mcp.json）
- `--scope user`: 全プロジェクトで利用可能

## 重要な注意事項

1. **Gドライブアクセス**: WSL環境からはGドライブが直接マウントされていないため、Windows形式のパス（`G:\`）を使用
2. **パス形式**: MCPサーバーによってWindows形式（`G:\`）とUnix形式（`/mnt/c/`）を適切に使い分ける
3. **権限**: 一部のMCPサーバーは管理者権限が必要な場合がある

## トラブルシューティング

### MCPツールが見つからない場合
1. `claude mcp list`で設定を確認
2. Claude Codeを再起動
3. 必要に応じてMCPサーバーを再追加

### Gドライブにアクセスできない場合
1. Google Drive for desktopが起動していることを確認
2. Gドライブが正しくマウントされていることを確認
3. Windows形式のパスを使用（`G:\\マイドライブ\\Obsidian Vault`）

## 今後の拡張

- Git Tools MCP（Python環境が必要）
- カスタムMCPサーバーの開発
- 追加のファイルシステムマウント

---
*このドキュメントはClaude CodeのMCP設定を永続化するために作成されました。*