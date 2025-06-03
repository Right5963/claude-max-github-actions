# MCP設定まとめ
作成日: 2025年6月1日

## 現在の設定状況

### 1. MCPサーバー起動 ✅
```bash
# 実行中のプロセス
claude mcp serve
# PID 973で起動中
```

### 2. Claude Desktop設定 ✅
`C:\Users\user\AppData\Roaming\Claude\claude_desktop_config.json`に登録済み：
```json
"claude-code": {
  "command": "wsl.exe",
  "args": [
    "bash",
    "-c",
    "source ~/.nvm/nvm.sh && /home/user/.nvm/versions/node/v18.20.8/bin/claude mcp serve"
  ]
}
```

### 3. 設定済みMCPサーバー（Claude Code CLI内）✅
```bash
# 確認コマンド
claude mcp list

# 結果
obsidian: G:\マイドライブ\Obsidian Vault
filesystem: /mnt/c/Claude Code/tool
filesystem-gdrive: G:\マイドライブ\Obsidian Vault
filesystem-mcp: /mnt/c/Claude Code/MCP
desktop-commander: デスクトップ操作
memory: セッション間メモリ
playwright: ブラウザ自動化
sqlite: 知識DB
note-api: Note.com API
```

## 重要なポイント

### 環境情報
- **OS**: WSL2 (Ubuntu)
- **Node.js**: v18.20.8 (nvm管理)
- **パス**: `/home/user/.nvm/versions/node/v18.20.8/bin/claude`

### パスと権限の注意点
1. **WSL環境**
   - Linux側のNode.jsを使用（Windows側ではない）
   - `which node`で確認: `/home/user/.nvm/versions/node/v18.20.8/bin/node`

2. **Windowsパス**
   - Gドライブ: `G:\マイドライブ\Obsidian Vault`
   - WSLからはマウントされていない（直接アクセス不可）

3. **権限**
   - ファイルアクセス権限は問題なし
   - WSL内での実行権限も正常

## 使用方法

### Claude Desktopから
1. Claude Desktopを起動
2. MCPツールが自動的に利用可能
3. 例：「Obsidianでメモを検索して」と依頼

### Claude Code CLIから
1. 標準ツール（Read/Write/Bash等）を使用
2. MCPサーバーの管理：
   ```bash
   claude mcp list    # 一覧表示
   claude mcp add     # 追加
   claude mcp remove  # 削除
   ```

## トラブルシューティング

### よくある問題
1. **MCPツールが見えない**
   - Claude Desktopを再起動
   - キャッシュをクリア

2. **パスエラー**
   - WSL/Windows形式の違いに注意
   - 絶対パスを使用

3. **Node.jsバージョン**
   - nvm/fnmで適切なバージョンを指定
   - 現在はv18.20.8を使用