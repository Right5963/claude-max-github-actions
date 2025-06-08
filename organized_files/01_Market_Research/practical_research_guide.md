# 実用的リサーチツールガイド（現実版）

## 🟢 今すぐ使える機能（設定不要）

### 1. 市場調査コマンド
```bash
# 国内市場
./specialized_research_bridge.sh yahoo_auction_ai "AIイラスト"
./specialized_research_bridge.sh fanza_doujin "AI CG"
./specialized_research_bridge.sh dlsite_search "AI"

# 海外市場  
./specialized_research_bridge.sh ebay_search "AI art"
./specialized_research_bridge.sh ai_art_platforms
```

### 2. Stable Diffusion調査
```bash
# モデル検索
./specialized_research_bridge.sh civitai_models checkpoint
./specialized_research_bridge.sh sd_webui_extensions
./specialized_research_bridge.sh prompt_sharing
```

### 3. 開発ツール調査
```bash
./specialized_research_bridge.sh mcp_awesome_list
./specialized_research_bridge.sh efficiency_tools
```

### 4. 学術検索（一部動作）
```bash
./research_mcp_bridge.sh arxiv_search "stable diffusion"  # API動作
./research_mcp_bridge.sh google_search "Claude API"       # ブラウザ開く
```

## 🟡 設定すれば使える機能

### Obsidian連携（既に設定済み）
```bash
./mcp_bridge_extended.sh obsidian_search "TAL"
./mcp_bridge_extended.sh obsidian_write "memo.md" "内容"
```

### メモリ管理（既に動作中）
```bash
./mcp_bridge_extended.sh memory_store "key" "value"
./mcp_bridge_extended.sh memory_list
```

## 🔴 実質使えない機能（複雑/有料）

- DALL-E画像生成（OpenAI API必要）
- Bright Dataスクレイピング（有料）
- WordPress自動投稿（サイト設定必要）
- Twitter API（認証必要）

## 💡 実用的なワークフロー

### 毎日のルーティン
```bash
#!/bin/bash
# daily_check.sh

echo "=== $(date) デイリーチェック ==="

# 1. Civitai新着モデル
./specialized_research_bridge.sh civitai_models checkpoint

# 2. 市場動向
./specialized_research_bridge.sh yahoo_auction_ai "AIイラスト"

# 3. 技術トレンド  
./research_mcp_bridge.sh arxiv_search "diffusion model"

# 結果をObsidianに保存
RESULT="今日のリサーチ結果..."
./mcp_bridge_extended.sh obsidian_write "Daily/$(date +%Y%m%d).md" "$RESULT"
```

### プロジェクト開始時
```bash
# 1. 市場調査
./specialized_research_bridge.sh market_research "AIアート"

# 2. 競合分析（各サイトを手動で確認）
./specialized_research_bridge.sh ai_art_market_analysis

# 3. 技術選定
./specialized_research_bridge.sh tech_stack_research
```

## ✅ 推奨事項

1. **ブラウザベースの機能を活用**
   - URL開いて手動確認が最も確実
   - 自動化より半自動化が現実的

2. **既存ツールと組み合わせ**
   - Obsidianにリサーチ結果を記録
   - メモリ管理で重要情報を保存

3. **段階的に拡張**
   - 必要になったらMCPサーバー追加
   - 無理に全部使おうとしない

## 🚀 次のステップ

1. まず`specialized_research_bridge.sh`を使い倒す
2. 結果をObsidianに蓄積する習慣をつける
3. 必要に応じてMCPサーバーを追加

これが現実的な使い方です！