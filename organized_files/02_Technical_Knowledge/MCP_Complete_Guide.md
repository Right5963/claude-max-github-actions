# MCP完全ガイド

統合日: 2025-06-06
統合元ファイル数: 5

## mcp_enhanced_research_guide

### 1. E-commerce/マーケットプレイス
- **eBay MCP** - オークション調査・価格分析
- **Bright Data MCP** - CAPTCHA突破・高度スクレイピング
- **Firecrawl MCP** - AI搭載データ抽出

### 2. 画像生成
- **DALL-E MCP** - OpenAI画像生成
- **Image Gen Server** - 汎用画像生成（Replicate Flux）
- **Stable Diffusion MCP** - SD WebUI統合

### AI画像市場調査
```bash
# 国内市場
./specialized_research_bridge.sh yahoo_auction_ai "AIイラスト"
./specialized_research_bridge.sh fanza_doujin "AI CG集"
./specialized_research_bridge.sh dlsite_search "AI画像集"
./specialized_re...[詳細省略]

### Stable Diffusion エコシステム
```bash
# モデル検索
./specialized_research_bridge.sh civitai_models checkpoint
./specialized_research_bridge.sh civitai_models lora
./specialized_research_bridge.sh civitai_extensions

# 技術情報
./specialize...[詳細省略]

### 開発ツール調査
```bash
# Claude/Cursor関連
./specialized_research_bridge.sh claude_code_plugins
./specialized_research_bridge.sh cursor_extensions
./specialized_research_bridge.sh obsidian_ai_plugins
./specialized_res...[詳細省略]

---

## mcp_full_bridge_TAL

## 問題の構造化
```tal
{問題定義 {
  現状: "9個のMCPサーバーが設定済みだが、AIから直接使用不可"
  目標: "全てのMCPツールと同等の機能を実現"
  
  {分析 {
    MCPサーバー一覧: [
      "obsidian",
      "filesystem", "filesystem-gdrive", "filesystem-mcp",
      "desktop-c...[詳細省略]

## 解決策の設計
```tal
{解決策アーキテクチャ {
  
  {レイヤー1: "コマンドルーター" {
    説明: "MCPコマンドを適切なバックエンドに振り分け"
    実装: "mcp_bridge.sh の拡張"
  }}
  
  {レイヤー2: "バックエンド実装" {
    PowerShell: "Windows API アクセス"
    Python: "複雑なロジック処理"
  ...[詳細省略]

## 実装計画


### 1. Desktop Commander ブリッジ
```tal
{desktop_commander_bridge {
  機能: [
    "スクリーンショット取得",
    "ウィンドウ操作",
    "システム情報取得"
  ]
  
  {実装方法 {
    screenshot: "PowerShell + .NET System.Drawing"
    window_control: "PowerShell + Win32 ...[詳細省略]

### 2. Memory MCP ブリッジ
```tal
{memory_bridge {
  機能: "セッション間でのデータ永続化"
  
  {実装方法 {
    storage: "SQLite データベース"
    location: "/mnt/c/Claude Code/tool/memory.db"
    interface: "キーバリューストア"
  }}
}}
```

---

## mcp_knowledge_for_obsidian

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
```bas...[詳細省略]

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

---

## mcp_problem_analysis_TAL

### 1. 現象の観察
```
観察 {
  状況: "claude mcp serve"は起動している
  設定: "claude mcp add"で9個のMCPサーバーを登録済み
  結果: AIからmcp_プレフィックスのツールが見えない
  
  推論 {
    可能性1: MCPツールへのアクセス権限の問題
    可能性2: AIの実行環境とMCPサーバー環境の分離
    可能性3: ツール登録の方法に問...[詳細省略]

### 2. アーキテクチャの分析
```
システム構造 {
  レイヤー1: Claude Desktop（MCPクライアント）
  レイヤー2: MCP Protocol（通信層）
  レイヤー3: Claude Code MCPサーバー
  レイヤー4: 登録されたMCPツール
  レイヤー5: Claude Code内のAI実行環境
  
  問題箇所 {
    レイヤー4→レイヤー5の接続が欠落
    理由: AIの実...[詳細省略]

### 3. 根本原因の特定
```
原因分析 {
  表面的原因: "mcp_"ツールが利用可能なツールリストに含まれていない
  
  中間的原因: {
    - AIの実行時にMCPツールが動的にロードされていない
    - ツール登録とAI環境の初期化が分離している
  }
  
  根本原因: {
    設計思想: Claude Code内のAIは標準ツールのみを使用する設計
    MCPツール: 外部クライ...[詳細省略]

### アプローチ1: 環境変数による解決
```
仮説 {
  IF: 特定の環境変数でMCPツールを有効化できる
  THEN: AI起動時にその環境変数を設定
  
  検証方法 {
    export CLAUDE_ENABLE_MCP_TOOLS=true
    export CLAUDE_MCP_TOOLS_PATH=/path/to/mcp/tools
    claude mcp serve --enable-ai-to...[詳細省略]

### アプローチ2: 設定ファイルによる解決
```
仮説 {
  IF: .mcp.jsonや設定ファイルでAI環境を制御できる
  THEN: ツール登録時にAI用の設定を追加
  
  検証方法 {
    作成: .mcp.json {
      "aiAccess": true,
      "exposeTools": ["obsidian", "filesystem"],
      "toolPrefix": "mcp_"
...[詳細省略]

---

## mcp_setup_summary

### 2. Claude Desktop設定 ✅
`C:\Users\user\AppData\Roaming\Claude\claude_desktop_config.json`に登録済み：
```json
"claude-code": {
  "command": "wsl.exe",
  "args": [
    "bash",
    "-c",
    "source ~/.nvm/nvm.sh && /home/user/.nvm/...[詳細省略]

### 3. 設定済みMCPサーバー（Claude Code CLI内）✅
```bash
# 確認コマンド
claude mcp list

# 結果
obsidian: G:\マイドライブ\Obsidian Vault
filesystem: /mnt/c/Claude Code/tool
filesystem-gdrive: G:\マイドライブ\Obsidian Vault
filesystem-mcp: /mnt/c/Claude Code/MCP
desktop...[詳細省略]

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
   - WSLからはマウントされていない...[詳細省略]

---

