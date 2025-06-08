# 修復済みシステム一覧（実用版）

## 🎯 主要システム（完全自動化済み）

### 1. 売上記録・分析システム
```bash
# 売上記録（簡易版）
python3 yahoo_sales_analyzer.py quick "アニメポスターA4" 2800

# 売上記録（詳細版）
python3 yahoo_sales_analyzer.py record "商品名" 価格 "タグ1,タグ2" "モデル名" "カテゴリ"

# 売上分析レポート生成
python3 yahoo_sales_analyzer.py analyze
```

### 2. ヤフオク分析システム
```bash
# ヤフオク市場調査（シンプル版、73行）
python3 yahoo_auction_simple.py

# 競合分析（フォールバックデータ使用）
python3 competitor_analyzer_unified.py
```

### 3. ワークフローシステム
```bash
# ポスター販売ワークフロー（リサーチ→プロンプト生成→記録）
python3 yahoo_poster_workflow.py "美少女 アニメ"

# タグからワイルドカード生成
python3 yahoo_tagger_workflow.py "1girl,anime style,masterpiece" "美少女"
```

### 4. AI支援システム
```bash
# CivitAIモデル推奨
python3 civitai_model_fetcher.py "anime poster"

# SD設定アドバイザー
python3 sd_intelligent_advisor.py "美少女 ポスター"

# LLM統合PDCA
python3 llm_pdca_automation.py aiplan "価格を2800円に" "週売上2万円"
python3 llm_pdca_automation.py do 3000 "新商品出品" "反応良好" "競合増加"
```

### 5. 売上改善統合システム
```bash
# ダッシュボード表示
python3 sales_improvement_core.py dashboard

# 売上記録
python3 sales_improvement_core.py sale 2800 "アニメポスター"

# PDCA開始
python3 sales_improvement_core.py pdca-start "価格最適化" "週2万円" "2800円で出品"
```

## 📋 実行順序（推奨）

### 日次ルーティン
1. `python3 yahoo_auction_simple.py` - 市場チェック
2. `python3 yahoo_poster_workflow.py "今日のキーワード"` - プロンプト生成
3. `python3 sd_intelligent_advisor.py "キーワード"` - SD設定確認
4. 画像生成後: `python3 yahoo_sales_analyzer.py quick "商品名" 価格`

### 週次分析
1. `python3 yahoo_sales_analyzer.py analyze` - 売上分析
2. `python3 sales_improvement_core.py dashboard` - 統合ダッシュボード
3. `python3 llm_pdca_automation.py aicheck` - AI支援評価

## 🚫 まだ修復が必要なシステム
- image_quality_evaluator.py（対話的選択が必要）
- obsidian_prompt_dict.py（対話的入力が必要）
- prompt_dictionary_to_wildcard.py（対話的選択が必要）
- yahoo_image_downloader.py（URLループ入力が必要）

## 💡 ヒント
- すべてのシステムはコマンドライン引数対応済み
- デフォルト値が設定されているため、引数なしでも動作
- 結果はJSONファイルに自動保存される