# リサーチツール クイックスタート

## 今すぐ使えるコマンド一覧

### 🎨 AI画像・同人市場調査
```bash
# ヤフオク
./specialized_research_bridge.sh yahoo_auction_ai "AIイラスト"

# 同人サイト
./specialized_research_bridge.sh fanza_doujin "AI"
./specialized_research_bridge.sh dlsite_search "AI画像集"

# 海外市場
./specialized_research_bridge.sh ebay_search "AI art"
./specialized_research_bridge.sh ai_art_platforms
```

### 🤖 Stable Diffusion関連
```bash
# Civitaiモデル検索
./specialized_research_bridge.sh civitai_models checkpoint
./specialized_research_bridge.sh civitai_models lora

# 拡張機能・プロンプト
./specialized_research_bridge.sh sd_webui_extensions
./specialized_research_bridge.sh prompt_sharing
```

### 📚 学術・技術情報
```bash
# arXiv論文検索（API動作）
./research_mcp_bridge.sh arxiv_search "diffusion model"

# 技術トレンド
./specialized_research_bridge.sh efficiency_tools
./specialized_research_bridge.sh mcp_awesome_list
```

### 💾 結果をObsidianに保存
```bash
# 調査結果を保存
./mcp_bridge_extended.sh obsidian_write "memo.md" "調査結果..."

# 既存ノート検索
./mcp_bridge_extended.sh obsidian_search "TAL"
```

## 使用例

**今日の新着チェック:**
```bash
./specialized_research_bridge.sh civitai_models checkpoint
```

**市場価格調査:**
```bash
./specialized_research_bridge.sh yahoo_auction_ai "AIポスター"
```

**技術論文調査:**
```bash
./research_mcp_bridge.sh arxiv_search "SDXL"
```

全て動作確認済みです！