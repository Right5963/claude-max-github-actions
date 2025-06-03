#!/bin/bash
# 日次ワークフロー統合テスト

echo "🚀 ヤフオクポスター販売 日次ワークフロー テスト"
echo "=================================================="
date

# 1. 市場調査
echo -e "\n📊 ステップ1: 市場調査"
echo "------------------------"
python3 yahoo_auction_simple.py

# 2. 競合分析
echo -e "\n🔍 ステップ2: 競合分析"
echo "------------------------"
python3 competitor_analyzer_unified.py

# 3. キーワード決定とプロンプト生成
echo -e "\n🎨 ステップ3: プロンプト生成"
echo "------------------------------"
python3 yahoo_poster_workflow.py "美少女 アニメ ファンタジー"

# 4. CivitAIモデル推奨
echo -e "\n🤖 ステップ4: AIモデル推奨"
echo "---------------------------"
python3 civitai_model_fetcher.py "anime fantasy poster"

# 5. SD設定アドバイス
echo -e "\n⚙️ ステップ5: SD設定最適化"
echo "---------------------------"
python3 sd_intelligent_advisor.py "美少女 ファンタジー"

# 6. 売上ダッシュボード確認
echo -e "\n💰 ステップ6: 売上状況確認"
echo "---------------------------"
python3 sales_improvement_core.py dashboard

echo -e "\n✅ ワークフローテスト完了"
echo "============================"
echo "次のステップ："
echo "1. Stable Diffusionで画像生成"
echo "2. 生成画像から上位20枚を選択"
echo "3. ヤフオクに出品"
echo "4. 売上を記録: python3 yahoo_sales_analyzer.py quick \"商品名\" 価格"