# 🗂️ システムファイル整理計画

## 📊 現状
- 総ファイル数: 529個のmdファイル + その他
- 状況: システム部品と不要ファイルが混在

## 🎯 整理方針
**システム構築に必要なコア部品のみ残す**

## 📋 保持対象（削除禁止）

### コアシステム部品
- perplexity_mcp_server.py
- market_api_mcp_server.js
- revenue_efficiency_research.sh
- ai_art_revenue_research.sh
- comprehensive_daily_research.sh
- instant_research_ai.py

### 設定・環境
- CLAUDE.md
- mcp_config.json
- .github/workflows/
- setup_*.bat

### MCPブリッジ
- mcp_bridge_*.sh
- specialized_research_bridge.sh

## 🗑️ 削除対象

### テスト・実験ファイル
- test_*
- *_test.*
- experimental_*

### バックアップ・重複
- *_backup.*
- *_old.*
- *_v2.*（最新版以外）

### 分析レポート重複
- popularity_research_report_* (最新以外)
- value_cycle_reproduction_guide_* (最新以外)
- yahoo_analysis_* (最新以外)

### 一時ファイル
- *.tmp
- *.cache
- screenshot_*

## 🚀 整理実行
1. コア部品特定
2. 重複・古いファイル削除
3. 目標: 30ファイル以下