# 強化版MCPリサーチツール完全ガイド

## 🚀 新規発見MCPサーバー

### 1. E-commerce/マーケットプレイス
- **eBay MCP** - オークション調査・価格分析
- **Bright Data MCP** - CAPTCHA突破・高度スクレイピング
- **Firecrawl MCP** - AI搭載データ抽出

### 2. 画像生成
- **DALL-E MCP** - OpenAI画像生成
- **Image Gen Server** - 汎用画像生成（Replicate Flux）
- **Stable Diffusion MCP** - SD WebUI統合

### 3. コンテンツ配信
- **WordPress MCP** - 自動投稿・管理
- **Notion MCP** - 知識ベース統合
- **Docswrite MCP** - ドキュメント自動化

## 📊 リサーチコマンド総覧

### 基本コマンド
```bash
# ヘルプ表示
./specialized_research_bridge.sh help
./research_mcp_bridge.sh help
```

### AI画像市場調査
```bash
# 国内市場
./specialized_research_bridge.sh yahoo_auction_ai "AIイラスト"
./specialized_research_bridge.sh fanza_doujin "AI CG集"
./specialized_research_bridge.sh dlsite_search "AI画像集"
./specialized_research_bridge.sh kindle_ai_books

# 海外市場
./specialized_research_bridge.sh ebay_search "AI art poster"
./specialized_research_bridge.sh mercari_search "AI illustration"
./specialized_research_bridge.sh ai_art_platforms
```

### Stable Diffusion エコシステム
```bash
# モデル検索
./specialized_research_bridge.sh civitai_models checkpoint
./specialized_research_bridge.sh civitai_models lora
./specialized_research_bridge.sh civitai_extensions

# 技術情報
./specialized_research_bridge.sh sd_webui_extensions
./specialized_research_bridge.sh sd_comfyui_nodes
./specialized_research_bridge.sh sd_trending_tech

# プロンプト研究
./specialized_research_bridge.sh prompt_sharing
```

### 開発ツール調査
```bash
# Claude/Cursor関連
./specialized_research_bridge.sh claude_code_plugins
./specialized_research_bridge.sh cursor_extensions
./specialized_research_bridge.sh obsidian_ai_plugins
./specialized_research_bridge.sh vscode_ai_extensions

# 効率化ツール
./specialized_research_bridge.sh efficiency_tools
./specialized_research_bridge.sh ai_dev_tools_trends
```

### MCP検索
```bash
# 公式ソース
./specialized_research_bridge.sh mcp_marketplace
./specialized_research_bridge.sh mcp_awesome_list

# カスタム検索
./specialized_research_bridge.sh mcp_github_search "image generation"
./specialized_research_bridge.sh mcp_npm_search "scraping"
```

### 学術・技術文献
```bash
# 論文検索
./research_mcp_bridge.sh arxiv_search "stable diffusion"
./research_mcp_bridge.sh pubmed_search "AI medical imaging"
./research_mcp_bridge.sh scholar_search "generative AI"

# ソーシャル分析
./research_mcp_bridge.sh twitter_trends
./research_mcp_bridge.sh reddit_subreddit "StableDiffusion"
./research_mcp_bridge.sh youtube_search "ComfyUI tutorial"
```

### 総合分析
```bash
# 市場全体
./specialized_research_bridge.sh ai_art_market_analysis
./specialized_research_bridge.sh market_research "AIイラスト集"

# 技術スタック
./specialized_research_bridge.sh tech_stack_research

# トピック深堀り
./research_mcp_bridge.sh research_topic "SDXL LoRA"
./research_mcp_bridge.sh trend_analysis "AI art"
```

## 💡 高度な活用テクニック

### 1. バッチリサーチ
```bash
# 複数プラットフォーム一括調査
for platform in yahoo_auction_ai fanza_doujin dlsite_search; do
    ./specialized_research_bridge.sh $platform "AI美少女"
    sleep 2
done
```

### 2. 定期監視スクリプト
```bash
#!/bin/bash
# daily_research.sh
echo "=== $(date) Daily Research ===" >> research_log.txt
./specialized_research_bridge.sh civitai_models checkpoint >> research_log.txt
./specialized_research_bridge.sh sd_trending_tech >> research_log.txt
./research_mcp_bridge.sh twitter_trends >> research_log.txt
```

### 3. 結果の自動保存
```bash
# Obsidianと連携
RESEARCH_RESULT=$(./research_mcp_bridge.sh arxiv_search "diffusion models")
./mcp_bridge_extended.sh obsidian_write "Research/$(date +%Y%m%d)_arxiv.md" "$RESEARCH_RESULT"
```

## 🔧 セットアップ手順

### 1. 基本MCPサーバー
```bash
./setup_all_mcp_servers.bat
```

### 2. リサーチ用MCP
```bash
./setup_research_mcp.sh
```

### 3. マーケットプレイスMCP
```bash
./setup_marketplace_mcp.sh
```

## 📈 推奨ワークフロー

### 新規プロジェクト開始時
1. 市場調査: `ai_art_market_analysis`
2. 技術調査: `tech_stack_research`
3. 競合分析: `market_research [具体的なジャンル]`
4. トレンド把握: `trend_analysis [キーワード]`

### 日常的なリサーチ
1. 新着チェック: Civitai, GitHub, Reddit
2. 売れ筋確認: 各販売プラットフォーム
3. 技術更新: SD extensions, MCP servers

### 月次レビュー
1. 市場動向の変化
2. 新規プラットフォーム
3. 規約・ガイドライン更新

## 🎯 特に注目すべきMCPサーバー

1. **Bright Data MCP** - 最強のスクレイピング能力
2. **Firecrawl MCP** - AI解析付きデータ抽出
3. **WordPress MCP** - コンテンツ自動配信
4. **DALL-E MCP** - 画像生成自動化
5. **Notion MCP** - 知識管理統合

これらのツールを組み合わせることで、リサーチから販売まで一貫した自動化が可能になります！