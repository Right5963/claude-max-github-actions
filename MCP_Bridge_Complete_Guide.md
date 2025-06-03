# Claude Code MCPブリッジ完全ガイド
作成日: 2025年6月1日
作成者: Claude Code AI

## 概要

Claude Code環境では、MCPツール（`mcp_`プレフィックス）に直接アクセスできないという制限があります。この問題を解決するため、標準ツールを使用してMCP機能を再現する「MCPブリッジシステム」を開発しました。

## 動作確認済み機能一覧

### ✅ 完全動作確認済み

#### 1. Obsidian操作
- `obsidian_search [検索語]` - ノート内検索
- `obsidian_read [パス]` - ノート読み込み  
- `obsidian_write [パス] [内容]` - ノート作成/更新
- `obsidian_list` - ノート一覧取得

#### 2. ファイルシステム
- `filesystem_list [パス]` - ディレクトリ一覧
- `filesystem_read [パス]` - ファイル読み込み
- `filesystem_write [パス] [内容]` - ファイル書き込み

#### 3. デスクトップ操作
- `desktop_screenshot` - スクリーンショット取得
- `desktop_sysinfo` - システム情報取得
- `desktop_windows` - ウィンドウ一覧

#### 4. メモリ管理（SQLite）
- `memory_init` - データベース初期化
- `memory_store [key] [value]` - データ保存
- `memory_get [key]` - データ取得
- `memory_list` - 保存データ一覧
- `memory_delete [key]` - データ削除

#### 5. ユーティリティ
- `weather_current [都市名]` - 現在の天気
- `sandbox_python [コード]` - Pythonコード実行（10秒タイムアウト付き）
- `browser_open [URL]` - ブラウザでURL開く
- `calendar_today` - 今日の日付表示

### ⚠️ 部分的に動作/要改善

#### 1. Web検索
- `web_search [クエリ]` - DuckDuckGo APIを使用するが結果が限定的

#### 2. Git操作
- `git_status`, `git_log`, `git_diff`, `git_branch` - リポジトリ内でのみ動作

#### 3. データ処理
- `pdf_extract [パス]` - popplerのインストールが必要
- `data_analyze [CSV]` - 基本的な分析のみ

## アーキテクチャ

```
Claude Code AI
    ↓
標準ツール（Task, Bash）
    ↓
MCPブリッジスクリプト
    ├── mcp_bridge.sh（基本版）
    ├── mcp_bridge_extended.sh（拡張版）
    └── mcp_bridge_advanced.sh（高度な機能）
         ↓
    バックエンド
    ├── PowerShell（Windows API）
    ├── Bash（Unix系コマンド）
    ├── Python（複雑な処理）
    └── SQLite（データ永続化）
```

## セットアップ方法

### 1. スクリプトの配置
すでに以下の場所に配置済み：
- `/mnt/c/Claude Code/tool/mcp_bridge.sh`
- `/mnt/c/Claude Code/tool/mcp_bridge_extended.sh`
- `/mnt/c/Claude Code/tool/mcp_bridge_advanced.sh`

### 2. 実行権限の付与
```bash
chmod +x "/mnt/c/Claude Code/tool/mcp_bridge*.sh"
```

### 3. 必要な設定

#### Gドライブアクセス（Obsidian用）
- Windows側でGoogle Drive for desktopがインストール済み
- Gドライブがマウントされている
- パス: `G:\マイドライブ\Obsidian Vault`

#### メモリDB
- 自動的に作成される
- 場所: `/mnt/c/Claude Code/tool/mcp_memory.db`

## 使用例

### Obsidian検索
```bash
/mnt/c/Claude\ Code/tool/mcp_bridge_extended.sh obsidian_search "TAL"
```

### スクリーンショット取得
```bash
/mnt/c/Claude\ Code/tool/mcp_bridge_extended.sh desktop_screenshot
# 結果: /mnt/c/Claude Code/tool/screenshot_YYYYMMDD_HHMMSS.png
```

### データ永続化
```bash
# 初期化
/mnt/c/Claude\ Code/tool/mcp_bridge_extended.sh memory_init

# 保存
/mnt/c/Claude\ Code/tool/mcp_bridge_extended.sh memory_store "project_name" "MCP Bridge Development"

# 取得
/mnt/c/Claude\ Code/tool/mcp_bridge_extended.sh memory_get "project_name"
```

### 天気情報
```bash
/mnt/c/Claude\ Code/tool/mcp_bridge_advanced.sh weather_current Tokyo
```

### Pythonコード実行
```bash
/mnt/c/Claude\ Code/tool/mcp_bridge_advanced.sh sandbox_python "print('Hello from MCP Bridge!')"
```

## 技術的詳細

### PowerShell経由のWindows API活用
```powershell
# スクリーンショット取得の例
Add-Type -AssemblyName System.Windows.Forms,System.Drawing
$bitmap = [System.Drawing.Bitmap]::new([System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Width, [System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Height)
```

### SQLiteによるデータ永続化
```sql
CREATE TABLE IF NOT EXISTS memory (
    key TEXT PRIMARY KEY,
    value TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### エンコーディング対策
```bash
# UTF-8エンコーディングの設定
powershell.exe -Command "[Console]::OutputEncoding = [System.Text.Encoding]::UTF8; ..."
```

## トラブルシューティング

### 文字化け
- PowerShellコマンドでUTF-8エンコーディングを明示的に設定

### パスの問題
- WSLパス: `/mnt/c/...`
- Windowsパス: `C:\...` または `G:\...`
- 必要に応じて`wslpath`コマンドで変換

### 権限エラー
- スクリプトに実行権限を付与: `chmod +x`
- Windows側の操作にはPowerShellを使用

## 今後の拡張予定

1. **API統合の強化**
   - より高度なWeb検索API
   - 金融データAPI
   - 機械翻訳API

2. **セキュリティ強化**
   - サンドボックス環境の改善
   - APIキーの安全な管理

3. **パフォーマンス最適化**
   - キャッシュ機構の実装
   - 並列処理の活用

## まとめ

このMCPブリッジシステムにより、Claude Code環境でも実質的にMCPツールと同等の機能を利用できるようになりました。制限を創造的に回避し、より強力なAI開発環境を実現しています。