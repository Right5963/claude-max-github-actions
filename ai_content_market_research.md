# AI生成コンテンツ市場リサーチガイド

## 🎨 販売プラットフォーム別戦略

### 1. ヤフオク - AIイラスト/ポスター販売
```bash
./specialized_research_bridge.sh yahoo_auction_ai "AIイラスト ポスター"
```
**リサーチポイント:**
- 価格帯: A3ポスター 1,000-5,000円
- 人気ジャンル: アニメ風、風景、抽象アート
- 成功要因: 高解像度、額装オプション、シリーズ化

### 2. FANZA同人 - AI CG集
```bash
./specialized_research_bridge.sh fanza_doujin "AI CG集"
```
**リサーチポイント:**
- 価格帯: 500-2,000円
- 枚数: 基本100枚以上
- 差別化: ストーリー性、キャラクター設定

### 3. DLsite - 同人作品
```bash
./specialized_research_bridge.sh dlsite_search "AI 画像集"
```
**リサーチポイント:**
- ジャンル: 成人向け、全年齢向け
- 形式: ZIP配布、PDF版
- 特典: 高解像度版、制作過程

### 4. Kindle出版 - AI技術書/画集
```bash
./specialized_research_bridge.sh kindle_ai_books
```
**リサーチポイント:**
- 技術書: プロンプト集、チュートリアル
- 画集: テーマ別作品集
- 価格: 99-2,500円

## 🤖 Stable Diffusion関連リサーチ

### モデル検索戦略
```bash
# Checkpointモデル（基本モデル）
./specialized_research_bridge.sh civitai_models checkpoint

# LoRAモデル（スタイル調整）
./specialized_research_bridge.sh civitai_models lora

# Embeddingモデル（特定概念）
./specialized_research_bridge.sh civitai_models embedding
```

### 必須拡張機能
```bash
# WebUI拡張機能
./specialized_research_bridge.sh sd_webui_extensions

# ComfyUIノード
./specialized_research_bridge.sh sd_comfyui_nodes
```

**推奨拡張機能:**
1. **ControlNet** - ポーズ/構図制御
2. **ADetailer** - 顔/手の自動修正
3. **Ultimate SD Upscale** - 高解像度化
4. **Dynamic Prompts** - プロンプト自動生成
5. **Civitai Helper** - モデル管理

## 💻 AI開発ツールリサーチ

### Claude Code効率化
```bash
./specialized_research_bridge.sh claude_code_plugins
```
**注目ツール:**
- セッション管理システム
- MCPブリッジ拡張
- 自動プロンプト最適化

### Cursor AI拡張
```bash
./specialized_research_bridge.sh cursor_extensions
```
**必須拡張:**
- AI Autocomplete強化
- コード生成テンプレート
- Git統合強化

### Obsidian AI活用
```bash
./specialized_research_bridge.sh obsidian_ai_plugins
```
**推奨プラグイン:**
- Text Generator - AI文章生成
- Smart Connections - AI関連付け
- Copilot - ChatGPT統合

## 🚀 効率化MCPツール検索

### 最新MCPサーバー発見
```bash
# 公式マーケットプレイス
./specialized_research_bridge.sh mcp_marketplace

# GitHub検索
./specialized_research_bridge.sh mcp_github_search "image generation"

# npmパッケージ
./specialized_research_bridge.sh mcp_npm_search "stable diffusion"

# キュレーションリスト
./specialized_research_bridge.sh mcp_awesome_list
```

## 📊 総合市場分析コマンド

### AI作品市場全体調査
```bash
./specialized_research_bridge.sh ai_art_market_analysis
```

### 特定ジャンル深堀り
```bash
./specialized_research_bridge.sh market_research "AIイラスト集 美少女"
./specialized_research_bridge.sh market_research "AI生成 写真集"
./specialized_research_bridge.sh market_research "StableDiffusion プロンプト集"
```

### 技術トレンド調査
```bash
./specialized_research_bridge.sh tech_stack_research
```

## 💡 リサーチのコツ

1. **価格調査時のポイント**
   - 販売数でソート
   - レビュー/評価を確認
   - 更新頻度をチェック

2. **競合分析**
   - トップセラーの共通点
   - 差別化ポイント
   - 価格設定戦略

3. **技術調査**
   - ダウンロード数/スター数
   - 最終更新日
   - Issues/PR活発度

4. **トレンド把握**
   - 週間/月間ランキング
   - 新着注目作品
   - コミュニティの話題

## 🔄 定期リサーチ推奨

### 日次チェック
- Civitai新着モデル
- 各販売サイトランキング

### 週次チェック
- GitHub/Reddit技術トレンド
- 新規MCPサーバー

### 月次チェック
- 市場全体の動向
- 新規参入プラットフォーム
- 規約/ガイドライン変更