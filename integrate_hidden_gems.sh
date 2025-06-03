#!/bin/bash
# 隠れた宝システムの統合スクリプト

echo "🎯 隠れた宝システム統合実行"
echo "=================================="
date

# 1. 市場の本質分析（週次実行推奨）
echo -e "\n📊 ステップ1: 市場の本質分析"
echo "------------------------------"
python3 popularity_research.py > "reports/market_insights_$(date +%Y%m%d).txt"
echo "✅ 市場分析レポート生成完了"

# 2. 価格戦略の思考補助（価格変更検討時）
echo -e "\n🧠 ステップ2: 価格戦略の思考補助"
echo "---------------------------------"
current_price=$(grep "平均価格" yahoo_simple_result.json 2>/dev/null | grep -o '[0-9]\+' | head -1 || echo "2800")
python3 thinking_core_simple.py "現在の価格${current_price}円は適切か" > "reports/price_thinking_$(date +%Y%m%d).txt"
echo "✅ 価格戦略思考分析完了"

# 3. 価値創造サイクルの理解（月次実行推奨）
echo -e "\n🔄 ステップ3: 価値創造サイクル分析"
echo "-----------------------------------"
python3 value_creation_cycle_analysis.py > "reports/value_cycle_$(date +%Y%m%d).txt"
echo "✅ 価値創造サイクル分析完了"

# 4. 売れ筋画像のリサーチ分析（常時有用）
echo -e "\n🎨 ステップ4: 売れる画像の本質分析"
echo "-----------------------------------"
python3 selling_image_research.py > "reports/image_research_$(date +%Y%m%d).txt"
echo "✅ 売れる画像研究レポート完了"

# 5. 統合レポートの作成
echo -e "\n📝 ステップ5: 統合インサイトレポート"
echo "-------------------------------------"
cat > "reports/integrated_insights_$(date +%Y%m%d).md" << EOF
# 統合インサイトレポート
生成日: $(date +"%Y-%m-%d %H:%M")

## 1. 市場の本質（popularity_research.py より）
$(tail -20 "reports/market_insights_$(date +%Y%m%d).txt" | head -10)

## 2. 価格戦略の考察（thinking_core_simple.py より）
$(tail -10 "reports/price_thinking_$(date +%Y%m%d).txt")

## 3. 価値創造の原則（value_creation_cycle_analysis.py より）
$(grep -A 5 "原則" "reports/value_cycle_$(date +%Y%m%d).txt" | head -10)

## 4. 今週の推奨アクション
1. 市場分析に基づく価格調整
2. 価値創造サイクルの実践
3. 売れ筋要素の画像生成への反映
EOF

echo "✅ 統合インサイトレポート生成完了"

# 6. レポートディレクトリの確認
echo -e "\n📁 生成されたレポート:"
echo "----------------------"
ls -la reports/*_$(date +%Y%m%d).*

echo -e "\n✨ 隠れた宝システムの統合実行完了！"
echo "次のステップ: reports/integrated_insights_$(date +%Y%m%d).md を確認"