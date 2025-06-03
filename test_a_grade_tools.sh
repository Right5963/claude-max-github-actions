#!/bin/bash
# A級ツール統合テストスクリプト

echo "🔧 A級ツール統合テスト開始"
echo "================================"
echo ""

# 1. tagger_unified.py テスト
echo "1️⃣ tagger_unified.py テスト"
echo "-----------------------------"
python3 tagger_unified.py "かわいい女の子 ファンタジー"
echo ""
sleep 1

# 2. wildcard_generator_unified.py テスト
echo "2️⃣ wildcard_generator_unified.py テスト"
echo "----------------------------------------"
if [ -d "test_wildcard_input" ]; then
    python3 wildcard_generator_unified.py test_wildcard_input A級テスト
else
    echo "⚠️ test_wildcard_inputディレクトリが見つかりません"
fi
echo ""
sleep 1

# 3. yahoo_quick_research.py テスト
echo "3️⃣ yahoo_quick_research.py テスト"
echo "----------------------------------"
python3 yahoo_quick_research.py "AI イラスト A4"
echo ""
sleep 1

# 4. content_creation_pipeline.sh テスト
echo "4️⃣ content_creation_pipeline.sh テスト"
echo "---------------------------------------"
if [ -x "./content_creation_pipeline.sh" ]; then
    ./content_creation_pipeline.sh prompt_variations "fantasy girl"
else
    echo "⚠️ content_creation_pipeline.shが実行可能でない"
    chmod +x content_creation_pipeline.sh
    ./content_creation_pipeline.sh prompt_variations "fantasy girl"
fi
echo ""
sleep 1

# 5. specialized_research_bridge.sh テスト
echo "5️⃣ specialized_research_bridge.sh テスト"
echo "-----------------------------------------"
if [ -x "./specialized_research_bridge.sh" ]; then
    ./specialized_research_bridge.sh civitai_models lora
else
    echo "⚠️ specialized_research_bridge.shが実行可能でない"
    chmod +x specialized_research_bridge.sh
    ./specialized_research_bridge.sh civitai_models lora
fi
echo ""

echo "================================"
echo "✅ A級ツール統合テスト完了!"
echo ""
echo "📋 チェックリスト:"
echo "- [ ] tagger_unified.py: タグ生成とワイルドカード保存"
echo "- [ ] wildcard_generator_unified.py: カテゴリ分類と出力"
echo "- [ ] yahoo_quick_research.py: ブラウザ起動と検索"
echo "- [ ] content_creation_pipeline.sh: プロンプトバリエーション"
echo "- [ ] specialized_research_bridge.sh: 外部サイト連携"
echo ""
echo "🎯 すべて正常に動作していれば、A級品質達成です！"